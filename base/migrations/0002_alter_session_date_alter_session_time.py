# Generated by Django 4.2.3 on 2023-08-23 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(auto_created=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='time',
            field=models.TimeField(auto_created=True),
        ),
    ]
