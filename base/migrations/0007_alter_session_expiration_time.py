# Generated by Django 4.2.6 on 2023-10-11 17:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_session_expiration_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='expiration_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 11, 17, 58, 50, 120773, tzinfo=datetime.timezone.utc)),
        ),
    ]
