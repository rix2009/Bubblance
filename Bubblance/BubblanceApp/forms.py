from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from BubblanceApp.models import BUser, Ambulance, EqInAmbulance, AmbulanceCrew, CustomerRequest
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
	

# class CustomerRequestForm(ModelForm):


