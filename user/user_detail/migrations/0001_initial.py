# Generated by Django 3.2.12 on 2022-09-26 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_tm', models.DateTimeField(auto_now=True)),
                ('created_tm', models.DateTimeField(auto_now_add=True)),
                ('user_email', models.EmailField(blank=True, default='', help_text='用户邮箱', max_length=254)),
                ('user_introduction', models.CharField(help_text='用户简介', max_length=128)),
                ('nickname', models.CharField(help_text='用户昵称', max_length=128)),
            ],
            options={
                'verbose_name': '用户详情信息',
                'verbose_name_plural': '用户详情信息',
                'db_table': 'user_detail',
            },
        ),
    ]
