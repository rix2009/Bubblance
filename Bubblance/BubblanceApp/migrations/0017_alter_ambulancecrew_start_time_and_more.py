# Generated by Django 4.2.3 on 2023-12-16 09:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0016_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 11, 15, 56, 779401)),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 11, 15, 56, 781101)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 16, 11, 15, 56, 781767)),
        ),
    ]
