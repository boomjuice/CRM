from django.shortcuts import render, redirect, HttpResponse
from database.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings


def student_index(request):
    return redirect('/student/my-courses/')


@login_required()
def my_courses(request):
    customer = request.user.customer
    if customer:
        student = Student.objects.get(customer=customer)
        class_list = ClassList.objects.filter(student=student)
    return render(request, 'student/my_courses.html', locals())


@login_required()
def my_class(request):
    customer = request.user.customer
    if customer:
        student = Student.objects.get(customer=customer)
        class_list = ClassList.objects.filter(student=student)
        students_list = {}
        for classes in class_list:
            students = Student.objects.filter(class_grade=classes)
            students_list[classes] = students
    else:
        return HttpResponse('你还不是学生')
    return render(request, 'student/my_class.html', locals())


@login_required()
def homework_manage(request, class_id):
    customer = request.user.customer
    if customer:
        student = Student.objects.get(customer=customer)
        class_grade = ClassList.objects.get(id=class_id)
        study_record_list = StudyRecord.objects.filter(student=student, course_record__class_grade=class_grade)
    else:
        return HttpResponse('你还不是学生')
    return render(request, 'student/homework_manage.html', locals())


@login_required()
def homework_upload(request, study_record_id):
    course_record = CourseRecord.objects.get(studyrecord=study_record_id)
    customer = request.user.customer
    student = Student.objects.get(customer=customer)
    uploaded_files = []
    study_record_upload_dir = os.path.join(settings.STUDENT_FILE_HOMEWORK, str(course_record))
    student_upload_dir = os.path.join(study_record_upload_dir, str(student.customer.name))
    if not os.path.isdir(study_record_upload_dir):
        os.mkdir(study_record_upload_dir)
    if os.path.isdir(student_upload_dir):
        uploaded_files = os.listdir(student_upload_dir)

    return render(request, 'student/homework_upload.html', locals())


@csrf_exempt
def homework_file_upload(request, study_record_id):
    customer = request.user.customer
    student = Student.objects.get(customer=customer)
    course_record = CourseRecord.objects.get(studyrecord=study_record_id)
    study_record_upload_dir = os.path.join(settings.STUDENT_FILE_HOMEWORK, str(course_record))
    student_upload_dir = os.path.join(study_record_upload_dir, str(student.customer.name))
    if not os.path.isdir(student_upload_dir):
        os.makedirs(student_upload_dir)
    file_obj = request.FILES.get('file')
    if len(os.listdir(student_upload_dir)) <= 4:
        with open(os.path.join(student_upload_dir, file_obj.name), 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
    else:
        return HttpResponse(json.dumps({'status': False, 'message': 'max upload limit is four'}))
    return HttpResponse(json.dumps({'status': True}))
