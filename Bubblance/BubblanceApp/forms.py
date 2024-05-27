from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from BubblanceApp.models import BUser, Ambulance, EqInAmbulance, AmbulanceCrew, CustomerRequest, Customer, Institution
from django.forms import ModelForm


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = BUser
		fields = ("username", "email", "password1", 
			"password2", "firstname", "lastname", 
			"id", "phonenumber", "usertype")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class UpdateUserForm(ModelForm):
	class Meta:	
		model = BUser
		fields = ("email", "firstname", "lastname",
				"phonenumber", "usertype")
		
	def save(self, commit=True):
		user = super(UpdateUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class NewAmbulanceForm(ModelForm):
	class Meta:
		model = Ambulance
		fields = ("ambulance_id", "ambulance_number")

	def save(self, commit=True):
		ambulance = super(NewAmbulanceForm, self).save(commit=False)
		if commit:
			ambulance.save()
		return ambulance


class NewCrewForm(ModelForm):
	class Meta:
		model = AmbulanceCrew
		fields = ('ambulance_id','driver_id')
		labels = {'ambulance_id': 'Ambulance', 'driver_id':'Driver'}

	def save(self, commit=True):
		crew = super(NewCrewForm, self).save(commit=False)
		if commit:
			crew.save()
		return crew


class EqupmentInAmbulanceForm(ModelForm):
	class Meta:
		model = EqInAmbulance
		fields = ("am_id", "eq_name", "amount")


	def __init__(self, *args, **kwargs):
		super(EqupmentInAmbulanceForm, self).__init__(*args, **kwargs)
		self.fields['amount'].label = 'Amount'
		self.fields['eq_name'].label = 'Equipment Name'


	
	def save(self, commit=True):
		eq = super(EqupmentInAmbulanceForm, self).save(commit=False)
		if commit:
			eq.save()
		return eq
	

class CustomerRequestForm(ModelForm):
	class Meta:
		model = CustomerRequest
		fields = ("customer_id","pick_from_institution", "pickup_institution", "pick_up_location",
			"num_of_floors", "elvator_in_home",
			"drop_at_institution","dropoff_institution","drop_of_location",
			"pick_up_time","return_trip", "return_trip_pick_up_time",
			"two_stuff_needed", "need_oxygen", "need_stretcher", "need_wheel_chair",
			"have_preferred_driver",  "preferred_driver")
	
	def __init__(self, *args, **kwargs):
		super(CustomerRequestForm, self).__init__(*args, **kwargs)
		self.fields['pick_from_institution'].label = 'Pick-up from an Instiitution?'
		self.fields['pickup_institution'].label = 'Choose a pick-up Instiitution'
		self.fields['pick_up_location'].label = 'Pick-up Address'
		self.fields['num_of_floors'].label = 'Number of floors at home'
		self.fields['elvator_in_home'].label = 'Home with Elevator?'
		self.fields['drop_at_institution'].label = 'Drop-off at an Instiitution?'
		self.fields['dropoff_institution'].label = 'Choose a drop-off Instiitution'
		self.fields['drop_of_location'].label = 'Drop-off Address'
		self.fields['pick_up_time'].label = 'Pick-up date and time'
		self.fields['return_trip'].label = 'Return trip needed?'
		self.fields['return_trip_pick_up_time'].label = 'Return trip pick-up date and time'
		self.fields['two_stuff_needed'].label = 'Need more than one stuff member?'
		self.fields['need_oxygen'].label = 'Need Oxygen?'
		self.fields['need_stretcher'].label = 'Need Stretcher?'
		self.fields['need_wheel_chair'].label = 'Need Wheel chair?'
		self.fields['have_preferred_driver'].label = 'Have a favorite driver?'
		self.fields['preferred_driver'].label = 'Pick a driver'

	def save(self, commit=True):
		req = super(CustomerRequestForm, self).save(commit=False)
		if commit:
			req.save()
		return req


class NewCustomer(ModelForm):
	class Meta:
		model = Customer
		fields = ("patient_name","contact_name", "contact_phone",
			"customer_type", "institution_id")

	def save(self, commit=True):
		customer = super(NewCustomer, self).save(commit=False)
		if commit:
			customer.save()
		return customer


class NewInstitution(ModelForm):
	class Meta:
		model = Institution
		fields = ("institution_name","institution_adress", "in_institution")

	def save(self, commit=True):
		institution = super(NewInstitution, self).save(commit=False)
		if commit:
			institution.save()
		return institution


class UpdateInstitutionForm(ModelForm):
	class Meta:	
		model = Institution
		fields = ("institution_name", "institution_adress", "in_institution",
				"status","inst_id")
		
	def save(self, commit=True):
		inst = super(UpdateInstitutionForm, self).save(commit=False)
		if commit:
			inst.save()
		return inst