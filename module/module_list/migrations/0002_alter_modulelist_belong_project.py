# Generated by Django 3.2.12 on 2023-03-23 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_list', '0001_initial'),
        ('module_list', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modulelist',
            name='belong_project',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='module', to='project_list.projectlist'),
        ),
    ]
