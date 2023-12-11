from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from BubblanceApp.models import BUser, Ambulance, Equipment, Eq_in_Ambulance
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
		labels = {"am_id": _("Ambulance"),
			"amount": _("Amount")}


	
	def save(self, commit=True):
		eq = super(EqupmentInAmbulanceForm, self).save(commit=False)
		if commit:
			eq.save()
		return eq