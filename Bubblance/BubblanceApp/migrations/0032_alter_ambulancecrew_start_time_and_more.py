# Generated by Django 5.0.7 on 2024-07-20 10:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0031_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 13, 52, 35, 616850)),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 13, 52, 35, 618853)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='drop_of_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 13, 52, 35, 619850)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 13, 52, 35, 619850)),
        ),
    ]
