# Generated by Django 3.2.12 on 2022-09-26 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_list', '0006_auto_20220926_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='tm_tm',
            field=models.CharField(default='2022-09-26 16:21:32.552048', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account',
            name='created_date_bj',
            field=models.CharField(default='2022-09-26 16:41:05', help_text='时间', max_length=128),
        ),
        migrations.AlterField(
            model_name='account',
            name='created_date_tm',
            field=models.CharField(default=1664181665626, help_text='时间', max_length=128),
        ),
    ]
