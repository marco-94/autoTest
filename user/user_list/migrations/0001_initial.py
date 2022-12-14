# Generated by Django 3.2.12 on 2022-09-26 15:16

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('updated_tm', models.DateTimeField(auto_now=True)),
                ('created_tm', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.AutoField(help_text='用户id', primary_key=True, serialize=False)),
                ('username', models.SlugField(help_text='用户名', max_length=128, unique=True)),
                ('password', models.CharField(help_text='用户密码', max_length=128)),
                ('is_disable', models.BooleanField(default=False, help_text='是否禁用')),
                ('is_delete', models.BooleanField(default=False, help_text='逻辑删除')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户基础信息',
                'verbose_name_plural': '用户基础信息',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_tm', models.DateTimeField(auto_now=True)),
                ('created_tm', models.DateTimeField(auto_now_add=True)),
                ('user_token', models.CharField(help_text='token', max_length=256)),
                ('user_info', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_base', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': '用户登录信息',
                'verbose_name_plural': '用户登录信息',
                'db_table': 'user_role',
            },
        ),
    ]
