# Generated by Django 3.2.12 on 2022-09-26 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_list', '0005_auto_20220926_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='created_date_bj',
            field=models.CharField(default='2022-09-26 16:21:00', help_text='时间', max_length=128),
        ),
        migrations.AlterField(
            model_name='account',
            name='created_date_tm',
            field=models.CharField(default=1664180460197, help_text='时间', max_length=128),
        ),
    ]
