from django.core.management.base import BaseCommand
from BubblanceApp.models import CustomerRide
import uuid

class Command(BaseCommand):
    help = 'Fill token field for existing CustomerRide objects'

    def handle(self, *args, **options):
        rides = CustomerRide.objects.filter(token__isnull=True)
        for ride in rides:
            ride.token = uuid.uuid4()
            ride.save()
            print(f'Ride {ride.cust_ride_id} token filled')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully filled token for {rides.count()} rides'))
