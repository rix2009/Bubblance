# Generated by Django 4.2.14 on 2024-07-27 13:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0040_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 27, 16, 57, 48, 280807)),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 27, 16, 57, 48, 281824)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='drop_of_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 27, 16, 57, 48, 281824)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 27, 16, 57, 48, 281824)),
        ),
    ]