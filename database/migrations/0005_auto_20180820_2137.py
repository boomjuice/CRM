# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-20 13:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20180820_1318'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.SmallIntegerField(choices=[(1, '学费'), (2, '退费'), (0, '报名费')])),
                ('amount', models.IntegerField(default=500, verbose_name='所缴费用')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('consultant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_agree', models.BooleanField(default=False)),
                ('contract_signed_date', models.DateTimeField(blank=True, null=True)),
                ('contract_approved', models.BooleanField(default=False)),
                ('contract_approved_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='customerinfo',
            options={'verbose_name': '客户信息'},
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='emergency_contact',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='gender',
            field=models.PositiveIntegerField(blank=True, choices=[(0, '男'), (1, ' 女')], null=True),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='id_num',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='classlist',
            name='class_type',
            field=models.SmallIntegerField(choices=[(0, '脱产'), (2, '网络班'), (1, '周末')], default=0),
        ),
        migrations.AlterField(
            model_name='customerfollowrecord',
            name='status',
            field=models.SmallIntegerField(choices=[(3, '已报名'), (2, '两周内报名'), (1, '一个月内报名'), (0, '近期无报名计划')]),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='contact_type',
            field=models.SmallIntegerField(choices=[(2, '手机'), (0, 'qq'), (1, '微信')]),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='source',
            field=models.SmallIntegerField(choices=[(1, '51CTO'), (0, 'QQ群'), (3, '知乎'), (4, '转介绍'), (5, '其他'), (2, '百度推广')]),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='status',
            field=models.SmallIntegerField(choices=[(2, '已退学'), (1, '已报名'), (0, '未报名')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='database.CustomerInfo'),
        ),
        migrations.AlterField(
            model_name='studyrecord',
            name='score',
            field=models.SmallIntegerField(choices=[(100, 'A+'), (40, 'C-'), (70, 'C+'), (90, 'A'), (0, 'N/A'), (85, 'B+'), (-50, 'D'), (-100, 'COPY'), (60, 'C'), (80, 'B'), (75, 'B-')], default=0),
        ),
        migrations.AlterField(
            model_name='studyrecord',
            name='show_status',
            field=models.SmallIntegerField(choices=[(2, '迟到'), (0, '缺勤'), (3, '早退'), (1, '已到')]),
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='class_grade',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.ClassList'),
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='consultant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.UserProfile'),
        ),
        migrations.AddField(
            model_name='studentenrollment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='enrollment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='database.StudentEnrollment'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract_template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='database.ContractTemplate'),
        ),
        migrations.AlterUniqueTogether(
            name='studentenrollment',
            unique_together=set([('customer', 'class_grade')]),
        ),
    ]
