from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('files', views.ListTextFiles.as_view()),
    path('files/<int:pk>', views.DetailTextFile.as_view()),
    path('scan', views.do_scan, name='scan'),
    path('count', views.do_count, name='count'),
    path('update_status/', views.update_status, name='update_status'),
    path('update_status_count/', views.update_status_count, name='update_status_count')
]