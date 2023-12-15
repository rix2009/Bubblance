from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from datetime import datetime


# Create your models here.


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
    # image = models.ImageField(default=None)


class Ambulance(models.Model):
    ambulance_id = models.AutoField(primary_key=True)
    ambulance_number = models.CharField(max_length=17)
    amb_availablity = models.BooleanField(default=True)


class AmbulanceCrew(models.Model):
    ambulance_id = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    driver_id = models.ForeignKey(BUser,related_name='related_primary_manual_roats', on_delete=models.CASCADE)
    sec_crew = models.ForeignKey(BUser,related_name='related_secondary_manual_roats', blank=True, null=True ,on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=datetime.now())
    end_time = models.DateTimeField(blank=True, null=True)


class EquipmentType(models.Model):
    eq_type_id = models.AutoField(primary_key=True)
    eq_type_name = models.CharField(max_length=100, unique=True)


class Equipment(models.Model):
    eq_id = models.AutoField(primary_key=True)
    eq_type_id = models.ForeignKey(EquipmentType, on_delete=models.CASCADE)
    eq_name = models.CharField(max_length=100, unique=True)


class Eq_in_Ambulance(models.Model):
    eq_id = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    am_id = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class Institution(models.Model):
    institution_name = models.CharField(max_length=100, unique=True)
    institution_adress = models.CharField(max_length=255)


class Customer(models.Model):
    class CustomerType(models.IntegerChoices):
        Private = 1
        Business = 2

    patient_name = models.CharField(max_length=60)
    contact_name = models.CharField(max_length=60)
    contact_phone = models.CharField(max_length=11)
    customer_type = models.IntegerField(choices=CustomerType.choices)
    institution_id = models.ForeignKey(Institution, blank=True, null=True, on_delete=models.CASCADE)


class CustomerRequest(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)    
    pick_up_location = models.CharField(max_length=100)
    drop_of_location = models.CharField(max_length=100)
    pick_up_time = models.DateTimeField(default=datetime.now())
    num_of_floors = models.PositiveIntegerField()
    devision_name = models.CharField(max_length=100, blank=True, null=True)
    elvator_in_home = models.BooleanField(default=False)
    need_oxygen = models.BooleanField(default=False)
    need_stretcher = models.BooleanField(default=False)
    need_wheel_chair = models.BooleanField(default=False)
    patient_weight = models.PositiveIntegerField()
    number_of_stuff_needed = models.PositiveIntegerField()
    preferred_driver = models.ForeignKey(BUser, blank=True, null=True, on_delete=models.CASCADE)
    return_trip = models.BooleanField(default=False)
    return_trip_pick_up_time = models.DateTimeField(blank=True, null=True)


class CustomerRide(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)    
    Am_id = models.ForeignKey(Ambulance, on_delete=models.CASCADE)
    customer_req = models.ForeignKey(CustomerRequest, on_delete=models.CASCADE)
    pick_up_location = models.CharField(max_length=100)
    drop_of_location = models.CharField(max_length=100)
    pick_up_time = models.DateTimeField(default=datetime.now())
    number_of_stuff_needed = models.PositiveIntegerField()
    

class EquipmentInRide(models.Model):
    eq_id = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    ride_id = models.ForeignKey(CustomerRide, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()