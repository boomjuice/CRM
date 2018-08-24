from django.shortcuts import render, reverse, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission
from database.models import *
from .form import *
from django import conf
import os
import json
from django.utils.timezone import datetime
from django.db.utils import IntegrityError
from django.core.mail import EmailMultiAlternatives


@login_required()
def dashboard(request):
    user_id = request.user.id
    my_order = StudentEnrollment.objects.filter(consultant_id=user_id, customer__status=1)

    return render(request, 'sale/dashboard.html', locals())


@login_required()
def stu_enrollment(request):
    """ 生成学员报名链接"""
    customers = CustomerInfo.objects.filter(status=0)
    class_list = ClassList.objects.all()
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        class_grade_id = request.POST.get('class_grade_id')
        try:
            enrollment_obj = StudentEnrollment.objects.create(
                customer_id=customer_id,
                class_grade_id=class_grade_id,
                consultant_id=request.user.id,
            )
            enrollment_link = 'localhost:8000%s' % reverse('enrollment',
                                                           kwargs={'enrollment_obj_id': enrollment_obj.id})
        except IntegrityError as e:
            enrollment_obj = StudentEnrollment.objects.get(customer_id=customer_id,
                                                           class_grade_id=class_grade_id, )
            if enrollment_obj.contract_agree:
                return redirect('/sale/stu_enrollment/%s/contract_audit/' % enrollment_obj.id)
    return render(request, 'sale/stu_enrollment.html', locals())


def enrollment(request, enrollment_obj_id):
    enrollment_obj = StudentEnrollment.objects.get(id=enrollment_obj_id)
    if enrollment_obj.contract_agree:
        return HttpResponse('捞仔想干嘛，给钱了就莫得了，慢慢等咯')
    if request.method == 'POST':
        customer_form = CustomerForm(instance=enrollment_obj.customer, data=request.POST)
        if customer_form.is_valid():
            for readonly_field in customer_form.Meta.readonly_fields:
                readonly_data = customer_form.cleaned_data.pop(readonly_field)
            CustomerInfo.objects.filter(studentenrollment=enrollment_obj_id).update(**customer_form.cleaned_data)
            enrollment_obj.contract_agree = True
            enrollment_obj.contract_signed_date = datetime.now()
            enrollment_obj.save()
            return HttpResponse('报名成功了，捞仔')
    else:
        customer_form = CustomerForm(instance=enrollment_obj.customer)

    # 列出上传文件
    uploaded_files = []
    enrollment_upload_dir = os.path.join(conf.settings.SALE_FILE_UPLOAD_DIR, enrollment_obj_id)
    if os.path.isdir(enrollment_upload_dir):
        uploaded_files = os.listdir(enrollment_upload_dir)
    return render(request, 'sale/enrollment.html', locals())


@csrf_exempt
def enrollment_file_upload(request, enrollment_obj_id):
    enrollment_upload_dir = os.path.join(conf.settings.SALE_FILE_UPLOAD_DIR, enrollment_obj_id)
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)
    file_obj = request.FILES.get('file')
    if len(os.listdir(enrollment_upload_dir)) <= 4:
        with open(os.path.join(enrollment_upload_dir, file_obj.name), 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
    else:
        return HttpResponse(json.dumps({'status': False, 'message': 'max upload limit is four'}))
    return HttpResponse(json.dumps({'status': True}))


@login_required()
def enrollment_contract_audit(request, enrollment_obj_id):
    enrollment_obj = StudentEnrollment.objects.get(id=enrollment_obj_id)
    if request.method == 'POST':
        enrollment_form = EnrollmentForm(instance=enrollment_obj, data=request.POST)
        if enrollment_form.is_valid():
            enrollment_form.save()
            stu_obj = Student.objects.get_or_create(customer=enrollment_obj.customer)[0]
            stu_obj.class_grade.add(enrollment_obj.class_grade_id)
            stu_obj.save()
            enrollment_obj.customer.status = 1
            enrollment_obj.customer.save()
            enrollment_obj.contract_approved_date = datetime.now()
            enrollment_obj.save()
            user = User()  # 创建用户名账号
            user.username = enrollment_obj.customer.contact
            password = enrollment_obj.customer.id_num + '.'
            user.set_password(password)
            user.save()
            student = Role.objects.get(name='Student')
            userprofile = UserProfile.objects.create(user=user, name=enrollment_obj.customer.name,
                                                     customer=enrollment_obj.customer)
            userprofile.role.add(student)
            from_email = conf.settings.DEFAULT_FROM_EMAIL
            subject = '恭喜你报名成功,以下是您的账号密码'
            text_content = '您的账号：%s, 您的密码：%s, ' % (enrollment_obj.customer.contact, password)
            msg = EmailMultiAlternatives(subject, text_content, from_email, ['741513373@qq.com'])
            msg.send()
            return redirect('/sale/')
    else:
        customer_form = CustomerForm(instance=enrollment_obj.customer)
        enrollment_form = EnrollmentForm(instance=enrollment_obj)
        enrollment_upload_dir = os.path.join(conf.settings.SALE_FILE_UPLOAD_DIR, enrollment_obj_id)
        confirm_img_list = os.listdir(enrollment_upload_dir)
    return render(request, 'sale/enrollment_contract_audit.html', locals())
