from django.template import Library
from database.models import *
from django.db.models import Q

register = Library()


@register.simple_tag()
def get_had_class(classes, user):
    count = CourseRecord.objects.filter(Q(class_grade=classes), Q(teacher=user)).count()
    return count


@register.simple_tag()
def get_approved_date(stu, classes_id):
    enrollment = StudentEnrollment.objects.get(Q(customer=stu.customer), Q(class_grade__id=classes_id))
    return enrollment.contract_approved_date


@register.simple_tag()
def get_have_class_time(student, class_id):
    count = StudyRecord.objects.filter(student=student, show_status__gt=0, course_record__class_grade=class_id).count()
    return count


@register.simple_tag()
def get_late_time(student, class_id):
    count = StudyRecord.objects.filter(student=student, show_status=2, course_record__class_grade=class_id).count()
    return count


@register.simple_tag()
def get_unable_time(student, class_id):
    count = StudyRecord.objects.filter(student=student, show_status=0, course_record__class_grade=class_id).count()
    return count
