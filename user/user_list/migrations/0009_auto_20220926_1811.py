# Generated by Django 3.2.12 on 2022-09-26 18:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_list', '0008_auto_20220926_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='created_date_bj',
        ),
        migrations.RemoveField(
            model_name='account',
            name='created_date_tm',
        ),
        migrations.RemoveField(
            model_name='account',
            name='time_tm',
        ),
        migrations.RemoveField(
            model_name='account',
            name='tm_tm',
        ),
    ]
