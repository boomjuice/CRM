"""CRM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from . import views as vs

urlpatterns = [
    url(r'^$', vs.student_index, name='student_index'),
    url(r'^my-courses/$', vs.my_courses, name='my_courses'),
    url(r'^my-class/$', vs.my_class, name='my_class'),
    url(r'^homework-manage/(?P<class_id>(\d+))/$', vs.homework_manage, name='homework_manage'),
    url(r'^upload-homework/(?P<study_record_id>(\d+))/$', vs.homework_upload, name='homework_upload'),
    url(r'^upload-homework/(?P<study_record_id>(\d+))/upload_file$', vs.homework_file_upload,
        name='homework_file_upload'),
]
