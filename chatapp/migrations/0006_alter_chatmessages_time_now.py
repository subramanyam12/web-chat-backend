# Generated by Django 4.2.5 on 2023-10-09 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0005_alter_chatmessages_time_now'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessages',
            name='time_now',
            field=models.DateTimeField(default='2023-10-09T14:18:45.861892'),
        ),
    ]