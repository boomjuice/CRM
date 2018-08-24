from django.shortcuts import render, redirect, reverse
from database.models import *
from django.contrib.auth.decorators import login_required
from .form import *
from django.db import IntegrityError


def teacher_index(request):
    return redirect(reverse('my_class'))


@login_required()
def my_class(request):
    teacher = request.user
    class_list = ClassList.objects.filter(teachers=teacher)
    return render(request, 'teacher/my_class.html', locals())


@login_required()
def course_record(request, class_id):
    class_grade = ClassList.objects.get(id=class_id)
    record_list = CourseRecord.objects.filter(class_grade__id=class_id, teacher=request.user)
    return render(request, 'teacher/courses_record.html', locals())


@login_required()
def student_list(request, class_id):
    teacher = request.user
    students_list = Student.objects.filter(class_grade=class_id)
    return render(request, 'teacher/student_list.html', locals())


@login_required()
def add_course_record(request, class_id):
    course_record_form = CourseRecordForm()
    if request.method == 'POST':
        course_record_form = CourseRecordForm(data=request.POST)
        if course_record_form.is_valid():
            classes = ClassList.objects.get(id=class_id)
            course_record_form.cleaned_data['class_grade'] = classes
            try:
                CourseRecord.objects.create(**course_record_form.cleaned_data)
                return redirect('/teacher/courses-record/%s/' % class_id)
            except IntegrityError as e:
                unique_error = '本课程本节次已存在'
    return render(request, 'teacher/add_courses_record.html', locals())
