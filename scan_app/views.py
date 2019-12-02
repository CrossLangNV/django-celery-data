from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from celery.result import AsyncResult
from .my_celery import scan, line_count_all
from django.db import models
from .models import TextFile
from .serializers import TextFileSerializer
from rest_framework import generics
from django import forms

class DirForm(forms.Form):
    scan_dir = forms.CharField(max_length=500)

class ListTextFiles(generics.ListCreateAPIView):
    queryset = TextFile.objects.all()
    serializer_class = TextFileSerializer

class DetailTextFile(generics.RetrieveUpdateDestroyAPIView):
    queryset = TextFile.objects.all()
    serializer_class = TextFileSerializer


def index(request):
    form = DirForm()
    return render(request, 'scan_app/index.html', {'form': form})

def do_scan(request):
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result
        form = DirForm()
        context = {
                'check_status': 1,
                'data': "",
                'state': 'START_SCAN',
                'task_id': job_id,
                'form': form
		}
        return render(request, 'scan_app/index.html', context)
    else:
        form = DirForm(request.POST)
        if form.is_valid():
            job = scan.delay(form.cleaned_data['scan_dir'])
            print ("Celery job ID:  {}.".format(job))
        return HttpResponseRedirect(reverse('scan') + '?job=' + job.id)

def do_count(request):
    text_files = TextFile.objects.all()
    text_files_names = [t.name for t in text_files]
    if 'job' in request.GET:
        job_id = request.GET['job']
        job = AsyncResult(job_id)
        data = job.result
        form = DirForm()
        context = {
                'check_status': 1,
                'data': "",
                'state': 'START_COUNT',
                'task_id': job_id,
                'files': text_files_names,
                'form': form
		}
        return render(request, 'scan_app/index.html', context)
    else:
        job = line_count_all.delay(text_files_names)
        print ("Celery job ID:  {}.".format(job))
        return HttpResponseRedirect(reverse('count') + '?job=' + job.id)

def update_status(request):
    print ("Update on: {}.".format(request.GET))
    if 'task_id' in request.GET.keys():
        task_id = request.GET['task_id']
        task = AsyncResult(task_id)
        result = task.result
        status = task.status
    else:
        status = 'UNDEFINED!'
        result = 'UNDEFINED!'
    try:
        json_data = {
            'check_status': 1,
            'status': status,
            'state': result['status']
            }
    except TypeError:
        json_data = {
            'check_status': 0,
            'status': status,
            'state': 'FINISHED',
            'files' : result
            }
        TextFile.objects.all().delete()
        for f in result:
            textfile = TextFile()
            textfile.name = f
            textfile.line_count = 0
            textfile.save()

    return JsonResponse(json_data)

def update_status_count(request):
    print ("Update count on: {}.".format(request.GET))
    if 'task_id' in request.GET.keys():
        task_id = request.GET['task_id']
        task = AsyncResult(task_id)
        result = task.children[0].get()
        status = task.status
    else:
        status = 'UNDEFINED!'
        result = 'UNDEFINED!'
    try:
        json_data = {
            'check_status': 1,
            'status': status,
            'state': result['status']
            }
    except TypeError:
        json_data = {
            'check_status': 0,
            'status': status,
            'state': 'COUNT_FINISHED',
            'count': result
            }
    return JsonResponse(json_data)