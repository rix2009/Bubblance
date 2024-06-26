# Generated by Django 4.2.4 on 2024-06-28 11:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0007_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 28, 14, 46, 10, 836236)),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 28, 14, 46, 10, 837238)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 28, 14, 46, 10, 838239)),
        ),
    ]
