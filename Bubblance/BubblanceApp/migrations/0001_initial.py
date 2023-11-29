# Generated by Django 4.2.4 on 2023-11-29 18:18

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firstname', models.CharField(max_length=30)),
                ('lastname', models.CharField(max_length=30)),
                ('israeliid', models.CharField(max_length=9, unique=True, validators=[django.core.validators.MinLengthValidator(9)])),
                ('phonenumber', models.CharField(max_length=10)),
                ('usertype', models.IntegerField(choices=[(1, 'Driver'), (2, 'Manager'), (3, 'Client')])),
                ('rememberme', models.BooleanField(default=False)),
                ('image', models.ImageField(default=None, upload_to='')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
