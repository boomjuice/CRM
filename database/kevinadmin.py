from .models import *
from KevinAdmin.admin_base import BaseKevinAdmin
from KevinAdmin.sites import site
from django.shortcuts import redirect


class CustomerAdmin(BaseKevinAdmin):
    list_display = ['id', 'name', 'source', 'contact_type', 'contact', 'consultant', 'consult_content', 'status',
                    'date']
    list_filter = ['source', 'consultant', 'status', 'date']
    search_fields = ['contact', 'consultant__name']
    readonly_fields = ['contact', 'status']
    filter_horizontal = ['consult_courses']
    actions = ['change_status', ]

    def change_status(self, request, queryset):
        queryset.update(status=0)
        return redirect('/kevin-admin/%s/%s' % (self.model._meta.app_label, self.model._meta.model_name))


site.register(UserProfile)
site.register(Branch)
site.register(ClassList)
site.register(CustomerInfo, CustomerAdmin)
site.register(CourseRecord)
site.register(Course)
site.register(Role)
site.register(Student)
site.register(StudyRecord)
site.register(CustomerFollowRecord)
site.register(Menus)
