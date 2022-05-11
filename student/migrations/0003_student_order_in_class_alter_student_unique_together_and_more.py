# Generated by Django 4.0.3 on 2022-05-09 14:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_alter_class_school_alter_class_teachers'),
        ('student', '0002_remove_student_origin_school_alter_student_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='order_in_class',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('origin_class', 'order_in_class')},
        ),
        migrations.CreateModel(
            name='StudentExel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel_file', models.FileField(upload_to='students_excels', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx'])])),
                ('class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.class', verbose_name='Class')),
            ],
        ),
    ]