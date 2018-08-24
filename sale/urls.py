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
from . import views as vs

urlpatterns = [
    url(r'^$', vs.dashboard, name='sale_index'),
    url(r'^stu_enrollment/$', vs.stu_enrollment, name='stu_enrollment'),
    url(r'^enrollment/(?P<enrollment_obj_id>(\d+))/$', vs.enrollment, name='enrollment'),
    url(r'^enrollment/(?P<enrollment_obj_id>(\d+))/file-upload$', vs.enrollment_file_upload,
        name='enrollment_file_upload'),
    url(r'^stu_enrollment/(?P<enrollment_obj_id>(\d+))/contract_audit/$', vs.enrollment_contract_audit,
        name='enrollment_contract_audit'),
]
