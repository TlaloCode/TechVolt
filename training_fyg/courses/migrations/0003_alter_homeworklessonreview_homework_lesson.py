# Generated by Django 3.2.14 on 2022-08-02 22:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20220801_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeworklessonreview',
            name='homework_lesson',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='homeworklessonreview', to='courses.homeworklesson', verbose_name='tarea leccion'),
        ),
    ]
