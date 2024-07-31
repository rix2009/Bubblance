from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
from django.utils import timezone
from BubblanceApp.models import CustomerRide, CustomerRequest, Customer, Institution, AmbulanceCrew, Status
import random

class Command(BaseCommand):
    help = 'Generates random rides'

    def add_arguments(self, parser):
        parser.add_argument('num_rides', type=int, help='Number of rides to generate')

    def handle(self, *args, **options):
        num_rides = options['num_rides']
        
        # List of addresses in Petah Tikva
        petah_tikva_addresses = [
            "Jabotinsky St 1, Petah Tikva",
            "Rothschild St 15, Petah Tikva",
            "Haim Ozer St 5, Petah Tikva",
            "Orlov St 10, Petah Tikva",
            "Pinsker St 3, Petah Tikva",
            "savion st 10, Petah Tikva",
            "amir binyamini St 2, Petah Tikva",
            "sokolov st 20, Petah Tikva",
            "David Wolfson St 52, petah tikva",
        ]
        institutions = list(Institution.objects.all())
        crews = list(AmbulanceCrew.objects.filter(end_time__isnull=True))
        customers = list(Customer.objects.all())

        current_time = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

        for _ in range(num_rides):
            customer = random.choice(customers)
            crew = random.choice(crews)
            institution = random.choice(institutions)

            # Randomly choose if pickup or drop-off is at an institution
            if random.choice([True, False]):
                pick_from_institution = True
                drop_at_institution = False
                pickup_institution = institution
                drop_of_institution = None
                pick_up_location = institution.institution_adress
                drop_of_location = random.choice(petah_tikva_addresses)
            else:
                pick_from_institution = False
                pickup_institution = None
                drop_at_institution = True
                drop_of_institution = institution
                pick_up_location = random.choice(petah_tikva_addresses)
                drop_of_location = institution.institution_adress

            # Generate random time for the ride
            ride_time = current_time + timedelta(minutes=random.randint(0, 1439))
            
            # Create CustomerRequest
            customer_request = CustomerRequest.objects.create(
                customer_id=customer,
                pick_from_institution = pick_from_institution,
                pickup_institution = pickup_institution,
                drop_at_institution = drop_at_institution,
                dropoff_institution = drop_of_institution,
                pick_up_location=pick_up_location,
                drop_of_location=drop_of_location,
                pick_up_time=ride_time,
                num_of_floors=random.randint(0, 5),
                elvator_in_home=random.choice([True, False]),
                need_oxygen=random.choice([True, False]),
                need_stretcher=random.choice([True, False]),
                need_wheel_chair=random.choice([True, False]),
                two_stuff_needed=random.choice([True, False]),
            )

            # Create CustomerRide
            CustomerRide.objects.create(
                customer_id=customer,
                Am_id=crew.ambulance_id,
                driver_id=crew.driver_id,
                customer_req=customer_request,
                pick_up_location=pick_up_location,
                drop_of_location=drop_of_location,
                pick_up_time=ride_time,
                drop_of_time=ride_time + timedelta(minutes=random.randint(30, 120)),
                number_of_stuff_needed=1 + customer_request.two_stuff_needed,
                status=Status.active
            )

            # Add some space between rides
            current_time += timedelta(minutes=random.randint(60, 180))


        self.stdout.write(self.style.SUCCESS(f'Successfully generated {num_rides} random rides'))