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
    url(r'^$', vs.teacher_index),
    url(r'^my-class/$', vs.my_class, name='my_class'),
    url(r'^courses-record/(?P<class_id>(\d+))/add/$', vs.add_course_record, name='add_course_record'),
    url(r'^courses-record/(?P<class_id>(\d+))/$', vs.course_record, name='course_record'),
    url(r'^my-class/(?P<class_id>(\d+))/student-list/$', vs.student_list, name='student_list'),
]
