from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from datetime import datetime


# Create your models here.
class Status(models.IntegerChoices):
    active = 1
    deactive = 2


class BUser(User):
    class UserType(models.IntegerChoices):
        Driver = 1
        Manager = 2
    
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    israeliid = models.CharField(max_length=9, validators=[MinLengthValidator(9)], unique=True)
    phonenumber = models.CharField(max_length=10)
    usertype = models.IntegerField(choices=UserType.choices)
    rememberme = models.BooleanField(default=False)
    status = models.IntegerField(choices=Status.choices, default=1)
    # image = models.ImageField(default=None)


class Ambulance(models.Model):
    ambulance_id = models.AutoField(primary_key=True)
    ambulance_number = models.CharField(max_length=17)
    amb_availablity = models.BooleanField(default=True)
    status = models.IntegerField(choices=Status.choices, default=1)


class AmbulanceCrew(models.Model):
    ambulance_id = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(BUser,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
    sec_crew = models.ForeignKey(BUser,related_name='related_secondary_manual_roats', blank=True, null=True ,on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(blank=True, null=True ,default=None)
    status = models.IntegerField(choices=Status.choices, default=1)


class EqInAmbulance(models.Model):
    eq_id = models.AutoField(primary_key=True)
    am_id = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    eq_name = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField()
    status = models.IntegerField(choices=Status.choices, default=1)


class Institution(models.Model):
    institution_name = models.CharField(max_length=100, unique=True)
    institution_adress = models.CharField(max_length=255)
    status = models.IntegerField(choices=Status.choices, default=1)
    in_institution = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)


class Customer(models.Model):
    class CustomerType(models.IntegerChoices):
        Private = 1
        Business = 2

    patient_name = models.CharField(max_length=60)
    contact_name = models.CharField(max_length=60)
    contact_phone = models.CharField(max_length=11)
    customer_type = models.IntegerField(choices=CustomerType.choices)
    institution_id = models.ForeignKey(Institution, blank=True, null=True, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=1)


class CustomerRequest(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)    
    pick_up_location = models.CharField(max_length=255)
    drop_of_location = models.CharField(max_length=255)
    pick_up_time = models.DateTimeField(default=datetime.now())
    num_of_floors = models.PositiveIntegerField()
    pick_from_institution = models.BooleanField(default=False)
    pickup_institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    drop_at_institution = models.BooleanField(default=False)
    dropoff_institution = models.ForeignKey(Institution, on_delete=models.CASCADE, blank=True, null=True)
    devision_name = models.CharField(max_length=100, blank=True, null=True)
    elvator_in_home = models.BooleanField(default=False)
    need_oxygen = models.BooleanField(default=False)
    need_stretcher = models.BooleanField(default=False)
    need_wheel_chair = models.BooleanField(default=False)
    patient_weight = models.PositiveIntegerField()
    two_stuff_needed = models.BooleanField(default=False)
    number_of_stuff_needed = models.PositiveIntegerField(blank=True, null=True)
    have_preferred_driver = models.BooleanField(default=False)
    preferred_driver = models.ForeignKey(BUser, blank=True, null=True, on_delete=models.CASCADE)
    return_trip = models.BooleanField(default=False)
    return_trip_pick_up_time = models.DateTimeField(blank=True, null=True)
    status = models.IntegerField(choices=Status.choices, default=1)


class CustomerRide(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)    
    Am_id = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    customer_req = models.ForeignKey(CustomerRequest, on_delete=models.CASCADE)
    pick_up_location = models.CharField(max_length=100)
    drop_of_location = models.CharField(max_length=100)
    pick_up_time = models.DateTimeField(default=datetime.now())
    number_of_stuff_needed = models.PositiveIntegerField()
    status = models.IntegerField(choices=Status.choices, default=1)
    charge_number = models.CharField(max_length=5, blank=True, null=True)


class EquipmentInRide(models.Model):
    eq_id = models.ForeignKey(EqInAmbulance, on_delete=models.CASCADE)
    ride_id = models.ForeignKey(CustomerRide, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.IntegerField(choices=Status.choices, default=1)