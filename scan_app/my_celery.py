from __future__ import absolute_import, unicode_literals
import os, glob, time
from celery import Celery
from celery import shared_task, current_task
from celery import signature
from celery import group
import pycountry
from pathlib import Path

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_app.settings')

app = Celery('scan_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@shared_task
def adding_task(x, y):
    return x + y

@shared_task
def line_count(filename):
    count = sum(1 for line in open(filename, encoding="utf8", errors='ignore'))
    current_task.update_state(
                state="PROGRESS",
                meta={
                    'status': 'COUNTING_SINGLE',
                    'count': count
                    }
                )
    return count

@shared_task
def line_count_all(files):
    current_task.update_state(
                state="PROGRESS",
                meta={
                    'status': 'COUNTING',
                    }
                )
    return group(line_count.s(f) for f in files)()

@shared_task
def scan(dirname):
    # extensions for all ISO 639-1 (2-letter) language codes
    lang_extensions = ['.' + lang.alpha_2 for lang in pycountry.languages if hasattr(lang, 'alpha_2')]
    files = [str(p.resolve()) for p in Path(dirname).glob("**/*") if p.is_file() and p.suffix in lang_extensions]
    current_task.update_state(
                state="PROGRESS",
                meta={
                    'files': files,
                    'status': 'COLLECTING',
                    }
                )
    time.sleep(2)
    return files
