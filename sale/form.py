from django.forms import ModelForm
from database.models import *


class EnrollmentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs.update({'disabled': 'true'})

        return ModelForm.__new__(cls)

    class Meta:
        model = StudentEnrollment
        fields = "__all__"
        exclude = ['contract_approved_date']
        readonly_fields = ['contract_signed_date', 'contract_agree',]


class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class': 'form-control'})
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs.update({'disabled': 'true'})

        return ModelForm.__new__(cls)

    class Meta:
        model = CustomerInfo
        fields = "__all__"
        exclude = ['consult_content', 'consult_courses', 'status']
        readonly_fields = ['contact_type', 'contact', 'consultant', 'referral_from', 'source']
