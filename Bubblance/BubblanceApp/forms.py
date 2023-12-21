from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from BubblanceApp.models import BUser, Ambulance, Equipment, Eq_in_Ambulance, AmbulanceCrew, CustomerRequest
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


class NewEquipmentForm(ModelForm):
	class Meta:
		model = Equipment
		fields = '__all__'

	def save(self, commit=True):
		eq = super(NewEquipmentForm, self).save(commit=False)
		if commit:
			eq.save()
		return eq


class EqupmentInAmbulanceForm(ModelForm):
	class Meta:
		model = Eq_in_Ambulance
		fields = ("am_id", "amount")


	def __init__(self, *args, **kwargs):
		super(EqupmentInAmbulanceForm, self).__init__(*args, **kwargs)
		self.fields['am_id'].label = 'Ambulance'
		self.fields['amount'].label = 'Amount'

	
	def save(self, commit=True):
		eq = super(EqupmentInAmbulanceForm, self).save(commit=False)
		if commit:
			eq.save()
		return eq
	

class NewCustomerRequest(ModelForm):
	class Meta:
		model = CustomerRequest
		fields = '__all__'

