# Generated by Django 4.2.5 on 2023-10-12 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0008_alter_chatmessages_time_now'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatmessages',
            name='time_now',
            field=models.DateTimeField(default='2023-10-12T11:53:17.781882'),
        ),
    ]
