# Generated by Django 4.2.5 on 2023-10-09 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0002_chatmessages_time_now'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatmessages',
            name='time_now',
        ),
    ]
