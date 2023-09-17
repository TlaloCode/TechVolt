# Generated by Django 3.2.14 on 2022-08-05 07:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0010_auto_20220805_0227'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeworkLessonReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='Indica si el registro debe ser tratado como activo. Desmarque esta opción en lugar de borrar el registro', verbose_name='active')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Fecha en que el registro fue creado.', verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, help_text='Última fecha en que el registro fue modificado', verbose_name='Última modificación')),
                ('qualification', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(0)], verbose_name='Calificación')),
                ('review', models.TextField(max_length=10000, verbose_name='Revision de la tarea')),
                ('created_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses_homeworklessonreview_created', to=settings.AUTH_USER_MODEL, verbose_name='Usuario creador')),
                ('homework_lesson_delivery', models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='homeworklessonreview', to='courses.homeworklessondelivery', verbose_name='Revisión de la tarea de lección')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses_homeworklessonreview_modified', to=settings.AUTH_USER_MODEL, verbose_name='Usuario editor')),
            ],
            options={
                'verbose_name': 'Revisión de tarea de la lección',
                'verbose_name_plural': 'Revisiones de tareas de las lecciones',
            },
        ),
    ]