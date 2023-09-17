# Generated by Django 3.2.14 on 2022-08-02 22:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_alter_homeworklessonreview_homework_lesson'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='homeworklessonreview',
            options={'verbose_name': 'Revisión de tarea de la lección', 'verbose_name_plural': 'Revisiones de tareas de las lecciones'},
        ),
        migrations.AlterField(
            model_name='homeworklessonreview',
            name='qualification',
            field=models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Calificacion'),
        ),
    ]