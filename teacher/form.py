from django.forms import ModelForm
from database.models import *


class CourseRecordForm(ModelForm):
    class Meta:
        model = CourseRecord
        fields = '__all__'
        exclude = ['class_grade', ]

    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})
            # if field_name in admin_class.readonly_fields:
            #     field_obj.widget.attrs.update({'disabled': 'true'})

        return ModelForm.__new__(cls)
