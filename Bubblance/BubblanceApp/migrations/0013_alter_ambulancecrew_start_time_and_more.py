# Generated by Django 4.2.4 on 2023-12-15 09:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0012_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 11, 29, 12, 922617)),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 11, 29, 12, 923618)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 15, 11, 29, 12, 924619)),
        ),
    ]
