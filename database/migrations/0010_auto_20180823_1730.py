# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-23 09:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_auto_20180823_1727'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('database_table_list', '可以查看kevinadmin每张表里所有的数据'), ('database_table_list_view', '可以访问kevinadmin表里每条数据的修改页'), ('database_table_list_change', '可以对kevinadmin表里的每条数据进行修改'), ('database_table_obj_add_view', '可以访问kevinadmin每张表的数据增加页'), ('database_table_obj_add', '可以对kevinadmin每张表进行数据添加'))},
        ),
        migrations.AlterField(
            model_name='classlist',
            name='class_type',
            field=models.SmallIntegerField(choices=[(0, '脱产'), (1, '周末'), (2, '网络班')], default=0),
        ),
        migrations.AlterField(
            model_name='customerfollowrecord',
            name='status',
            field=models.SmallIntegerField(choices=[(3, '已报名'), (1, '一个月内报名'), (0, '近期无报名计划'), (2, '两周内报名')]),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='contact_type',
            field=models.SmallIntegerField(choices=[(0, 'qq'), (2, '手机'), (1, '微信')]),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='gender',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '男'), (1, ' 女')], null=True),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='source',
            field=models.SmallIntegerField(choices=[(4, '转介绍'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (0, 'QQ群'), (5, '其他')]),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '未报名'), (2, '已退学'), (1, '已报名')]),
        ),
        migrations.AlterField(
            model_name='paymentrecord',
            name='payment_type',
            field=models.SmallIntegerField(choices=[(2, '退费'), (0, '报名费'), (1, '学费')]),
        ),
        migrations.AlterField(
            model_name='studyrecord',
            name='score',
            field=models.SmallIntegerField(choices=[(90, 'A'), (85, 'B+'), (100, 'A+'), (70, 'C+'), (-50, 'D'), (0, 'N/A'), (75, 'B-'), (80, 'B'), (40, 'C-'), (60, 'C'), (-100, 'COPY')], default=0),
        ),
        migrations.AlterField(
            model_name='studyrecord',
            name='show_status',
            field=models.SmallIntegerField(choices=[(0, '缺勤'), (3, '早退'), (1, '已到'), (2, '迟到')]),
        ),
    ]
