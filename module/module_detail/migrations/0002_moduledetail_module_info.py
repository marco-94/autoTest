# Generated by Django 3.2.12 on 2023-03-22 17:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('module_list', '0001_initial'),
        ('module_detail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moduledetail',
            name='module_info',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='module', to='module_list.modulelist'),
        ),
    ]
