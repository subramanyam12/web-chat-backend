# Generated by Django 4.2.5 on 2023-10-11 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0007_alter_chatmessages_time_now'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessages',
            name='time_now',
            field=models.DateTimeField(default='2023-10-11T17:11:19.103175'),
        ),
    ]
