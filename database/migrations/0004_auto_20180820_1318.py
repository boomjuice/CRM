# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-20 05:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0003_auto_20180817_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlist',
            name='class_type',
            field=models.SmallIntegerField(choices=[(2, '网络班'), (1, '周末'), (0, '脱产')], default=0),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='contact_type',
            field=models.SmallIntegerField(choices=[(1, '微信'), (0, 'qq'), (2, '手机')]),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='source',
            field=models.SmallIntegerField(choices=[(4, '转介绍'), (2, '百度推广'), (0, 'QQ群'), (3, '知乎'), (5, '其他'), (1, '51CTO')]),
        ),
        migrations.AlterField(
            model_name='studyrecord',
            name='score',
            field=models.SmallIntegerField(choices=[(-50, 'D'), (75, 'B-'), (80, 'B'), (60, 'C'), (-100, 'COPY'), (90, 'A'), (70, 'C+'), (85, 'B+'), (100, 'A+'), (40, 'C-'), (0, 'N/A')], default=0),
        ),
        migrations.AlterField(
            model_name='studyrecord',
            name='show_status',
            field=models.SmallIntegerField(choices=[(0, '缺勤'), (3, '早退'), (1, '已到'), (2, '迟到')]),
        ),
    ]
