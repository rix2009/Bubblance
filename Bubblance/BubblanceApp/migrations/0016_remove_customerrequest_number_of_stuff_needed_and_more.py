# Generated by Django 4.2.3 on 2024-07-12 12:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0015_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerrequest',
            name='number_of_stuff_needed',
        ),
        migrations.RemoveField(
            model_name='customerrequest',
            name='patient_weight',
        ),
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 12, 15, 1, 2, 763358)),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_type',
            field=models.IntegerField(choices=[(0, 'Private'), (1, 'Business')], default=0),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 12, 15, 1, 2, 765467)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='drop_of_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 12, 15, 1, 2, 765467)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 12, 15, 1, 2, 765467)),
        ),
    ]
