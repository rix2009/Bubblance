# Generated by Django 5.0.7 on 2024-07-20 10:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0027_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 13, 35, 54, 909290)),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 13, 35, 54, 910290)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='drop_of_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 13, 35, 54, 911335)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 20, 13, 35, 54, 911335)),
        ),
    ]