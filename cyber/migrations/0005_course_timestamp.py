# Generated by Django 5.0.6 on 2024-10-20 16:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyber', '0004_alter_course_assigned_to_alter_course_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
