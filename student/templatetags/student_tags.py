from django.template import Library
from database.models import *
from django.db.models.aggregates import Sum

register = Library()


@register.simple_tag()
def get_had_class(obj, user):
    customer = user.customer
    student = Student.objects.filter(customer=customer)
    count = StudyRecord.objects.filter(student=student, show_status__gt=0, course_record__class_grade=obj).count()
    return count


@register.simple_tag()
def get_had_student_class(student, classes):
    count = StudyRecord.objects.filter(student=student, show_status__gt=0, course_record__class_grade=classes).count()
    return count


@register.simple_tag()
def get_score_ranking(student,classes):
    score_list = Student.objects.filter(class_grade=classes).annotate(totalscore=Sum('studyrecord__score')). \
        values('customer').order_by('-totalscore')
    score_ranking_dict = {}
    i = 1
    for score in score_list:
        score_ranking_dict[i] = score
        i += 1
    for k, v in score_ranking_dict.items():
        if v['customer'] == student.customer.id:
            rank = k
    return rank
