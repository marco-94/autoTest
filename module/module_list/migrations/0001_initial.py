# Generated by Django 3.2.12 on 2023-03-22 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_list', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleList',
            fields=[
                ('updated_tm', models.DateTimeField(auto_now=True)),
                ('created_tm', models.DateTimeField(auto_now_add=True)),
                ('module_id', models.AutoField(help_text='模块id', primary_key=True, serialize=False)),
                ('module_name', models.SlugField(help_text='模块名', max_length=128, unique=True)),
                ('module_version', models.CharField(blank=True, default='V0.0.1', help_text='模块版本号', max_length=128)),
                ('module_desc', models.CharField(help_text='模块描述', max_length=512, null=True)),
                ('is_disable', models.BooleanField(default=False, help_text='是否禁用')),
                ('is_delete', models.BooleanField(default=False, help_text='逻辑删除')),
                ('editor', models.CharField(default='admin', help_text='编辑者', max_length=128)),
                ('belong_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project_list.projectlist')),
            ],
            options={
                'verbose_name': '模块基本信息',
                'verbose_name_plural': '模块基本信息',
                'db_table': 'module',
            },
        ),
    ]
