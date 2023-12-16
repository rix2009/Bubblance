# Generated by Django 4.2.4 on 2023-12-14 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0010_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eq_in_ambulance',
            old_name='Am_id',
            new_name='am_id',
        ),
        migrations.AlterField(
            model_name='ambulancecrew',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 19, 3, 15, 957525)),
        ),
        migrations.AlterField(
            model_name='customerrequest',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 19, 3, 15, 959527)),
        ),
        migrations.AlterField(
            model_name='customerride',
            name='pick_up_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 19, 3, 15, 959527)),
        ),
    ]