from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,

    )
    name = models.CharField(max_length=64, verbose_name="姓名")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    role = models.ManyToManyField("Role", blank=True, null=True)
    customer = models.OneToOneField('CustomerInfo', blank=True, null=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    class Meta:
        permissions = (
            ('database_table_list', '可以查看kevinadmin每张表里所有的数据'),
            ('database_table_list_view', '可以访问kevinadmin表里每条数据的修改页'),
            ('database_table_list_change', '可以对kevinadmin表里的每条数据进行修改'),
            ('database_table_obj_add_view', '可以访问kevinadmin每张表的数据增加页'),
            ('database_table_obj_add', '可以对kevinadmin每张表进行数据添加'),
            ('database_table_obj_delete', '可以对kevinadmin每张表进行数据删除'),
            ('database_table_obj_delete_view', '可以对kevinadmin删除时查看所关联的数据'),
             )

        #
        # class UserProfile(models.Model):
        #     """用户信息表"""
        #     user = models.OneToOneField(User)
        #     name = models.CharField(max_length=64, verbose_name="姓名")
        #     role = models.ManyToManyField('Role', blank=True)
        #     customer = models.OneToOneField('CustomerInfo', null=True, blank=True)
        #
        #     def __str__(self):
        #         return self.name


class Role(models.Model):
    """角色表"""
    name = models.CharField(max_length=64, unique=True)
    menus = models.ManyToManyField('Menus')

    def __str__(self):
        return self.name


class CustomerInfo(models.Model):
    """客户信息表"""
    name = models.CharField(max_length=64, default=None)
    contact_type_choices = {
        (0, 'qq'),
        (1, '微信'),
        (2, '手机'),
    }
    contact_type = models.SmallIntegerField(choices=contact_type_choices)
    contact = models.CharField(max_length=64, unique=True)
    source_choices = {
        (0, 'QQ群'),
        (1, '51CTO'),
        (2, '百度推广'),
        (3, '知乎'),
        (4, '转介绍'),
        (5, '其他')
    }
    source = models.SmallIntegerField(choices=source_choices)
    referral_from = models.ForeignKey('self', blank=True, null=True)
    consult_courses = models.ManyToManyField('Course', verbose_name='咨询课程')
    consult_content = models.TextField(verbose_name='咨询描述')
    consultant = models.ForeignKey('UserProfile', verbose_name='课程顾问')
    status_choices = {
        (0, '未报名'),
        (1, '已报名'),
        (2, '已退学')
    }
    id_num = models.CharField(max_length=128, null=True, blank=True)
    emergency_contact = models.PositiveIntegerField(blank=True, null=True)
    status = models.SmallIntegerField(choices=status_choices)
    gender_choices = {(0, '男'), (1, ' 女')}
    gender = models.PositiveIntegerField(blank=True, null=True, choices=gender_choices)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = '客户信息'

    def __str__(self):
        return self.name


class Student(models.Model):
    """学员表"""
    customer = models.OneToOneField("CustomerInfo")
    class_grade = models.ManyToManyField('ClassList')

    def __str__(self):
        return '%s' % self.customer


class CustomerFollowRecord(models.Model):
    """客户跟踪记录表"""
    customer = models.ForeignKey('CustomerInfo')
    content = models.TextField(verbose_name='跟踪内容')
    user = models.ForeignKey('UserProfile', verbose_name='跟进人')
    status_choices = {
        (0, '近期无报名计划'),
        (1, '一个月内报名'),
        (2, '两周内报名'),
        (3, '已报名'),
    }
    status = models.SmallIntegerField(choices=status_choices)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content


class Course(models.Model):
    """课程表"""
    name = models.CharField(max_length=64, verbose_name='课程名称', unique=True)
    price = models.PositiveSmallIntegerField()
    period = models.PositiveSmallIntegerField(verbose_name='课程周期(月)', default=5)
    outline = models.TextField(verbose_name='课程大纲')

    def __str__(self):
        return self.name


class ClassList(models.Model):
    """班级列表"""
    branch = models.ForeignKey('Branch')
    course = models.ForeignKey('Course')
    class_type_choices = {
        (0, '脱产'),
        (1, '周末'),
        (2, '网络班'),
    }
    class_type = models.SmallIntegerField(choices=class_type_choices, default=0)
    semester = models.SmallIntegerField(verbose_name='学期')
    contract_template = models.ForeignKey('ContractTemplate', blank=True, null=True)
    teachers = models.ManyToManyField('UserProfile', verbose_name='讲师')
    start_date = models.DateField("开班日期")
    graduate_date = models.DateField('毕业日期', blank=True, null=True)

    class Meta:
        unique_together = ('branch', 'course', 'semester', 'class_type')

    def __str__(self):
        return "{0}({1})".format(self.course.name, self.semester)


class CourseRecord(models.Model):
    """上课记录"""
    class_grade = models.ForeignKey('ClassList', verbose_name='上课班级')
    day_num = models.PositiveSmallIntegerField(verbose_name='课程节次')
    teacher = models.ForeignKey('UserProfile')
    title = models.CharField(max_length=64, verbose_name='本节主题')
    content = models.TextField('本节内容')
    has_homework = models.BooleanField('本节有作业', default=True)
    homework = models.TextField('作业需求', blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('class_grade', 'day_num')

    def __str__(self):
        return "{0}第{1}节".format(self.class_grade, self.day_num)


class StudyRecord(models.Model):
    """学习记录表"""
    course_record = models.ForeignKey('CourseRecord')
    student = models.ForeignKey('Student')
    score_choices = {
        (100, "A+"),
        (90, "A"),
        (85, "B+"),
        (80, "B"),
        (75, "B-"),
        (70, "C+"),
        (60, "C"),
        (40, "C-"),
        (-50, "D"),
        (0, "N/A"),
        (-100, "COPY"),
    }
    score = models.SmallIntegerField(choices=score_choices, default=0)
    show_choices = {
        (0, '缺勤'),
        (1, '已到'),
        (2, '迟到'),
        (3, '早退'),
    }
    show_status = models.SmallIntegerField(choices=show_choices)
    note = models.CharField("成绩备注", blank=True, null=True, max_length=1024)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('course_record', 'student')

    def __str__(self):
        return "{0} {1} {2}".format(self.course_record, self.student, self.score)


class Branch(models.Model):
    """校区"""
    name = models.CharField(max_length=64, unique=True)
    addr = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Menus(models.Model):
    """动态菜单"""
    name = models.CharField(max_length=64)
    url_type_choices = {
        (0, 'absolute'),
        (1, 'dynamic'),
    }
    url_type = models.SmallIntegerField(choices=url_type_choices, default=0)
    url_name = models.CharField(max_length=128)

    class Meta:
        unique_together = ('name', 'url_name')

    def __str__(self):
        return self.name


class ContractTemplate(models.Model):
    """存储合同模板"""
    name = models.CharField(max_length=64)
    content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.name


class StudentEnrollment(models.Model):
    """学员报名表"""
    customer = models.ForeignKey('CustomerInfo')
    class_grade = models.ForeignKey('ClassList')
    consultant = models.ForeignKey('UserProfile')
    contract_agree = models.BooleanField(default=False)
    contract_signed_date = models.DateTimeField(blank=True, null=True)
    contract_approved = models.BooleanField(default=False)
    contract_approved_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('customer', 'class_grade')

    def __str__(self):
        return '%s' % self.customer


class PaymentRecord(models.Model):
    """缴费记录表"""
    enrollment = models.ForeignKey('StudentEnrollment')
    payment_type_choices = {
        (0, '报名费'),
        (1, '学费'),
        (2, '退费'),
    }
    payment_type = models.SmallIntegerField(choices=payment_type_choices)
    amount = models.IntegerField('所缴费用', default=500)
    consultant = models.ForeignKey('UserProfile')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.enrollment
