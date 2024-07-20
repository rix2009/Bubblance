from django.db import migrations
import uuid

def gen_uuid(apps, schema_editor):
    CustomerRide = apps.get_model('BubblanceApp', 'CustomerRide')
    for row in CustomerRide.objects.all():
        row.token = uuid.uuid4()
        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('BubblanceApp', '0029_customerride_token_alter_ambulancecrew_start_time_and_more'),
    ]

    operations = [
        migrations.RunPython(gen_uuid),
    ]