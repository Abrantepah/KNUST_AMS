# Generated by Django 4.2.6 on 2023-10-11 16:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_attendance_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 11, 16, 14, 44, 162059, tzinfo=datetime.timezone.utc)),
        ),
    ]
