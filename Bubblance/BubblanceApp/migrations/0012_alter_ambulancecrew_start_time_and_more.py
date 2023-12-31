# Generated by Django 4.2.4 on 2023-12-14 17:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0011_rename_am_id_eq_in_ambulance_am_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 19, 43, 42, 907244)),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 19, 43, 42, 908266)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 19, 43, 42, 909271)),
        ),
    ]
