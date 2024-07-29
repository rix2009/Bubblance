from django import forms
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from BubblanceApp.models import BUser, Ambulance, EqInAmbulance, AmbulanceCrew, CustomerRequest, Customer, Institution, CustomerRide
from django.forms import ModelForm, HiddenInput, DateTimeInput
from django.core.validators import EMPTY_VALUES
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput, DateTimePickerInput, MonthPickerInput, YearPickerInput
BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))



class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = BUser
		fields = ("username", "email", "password1", 
			"password2", "firstname", "lastname", 
			"israeliid", "phonenumber", "usertype")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class UpdateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = BUser
        fields = ['username', 'email', 'firstname', 'lastname', 'israeliid', 'phonenumber', 'usertype']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        editable_fields = ['username', 'email', 'firstname', 'lastname', 'phonenumber', 'usertype']
        for field in self.fields:
            if field not in editable_fields and field != 'password':
                self.fields[field].widget.attrs['readonly'] = True



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
        fields = ("customer_id", "pick_from_institution", "pickup_institution", "pick_up_location",
                  "num_of_floors", "elvator_in_home", "drop_at_institution", "dropoff_institution",
                  "drop_of_location", "pick_up_time", "return_trip", "return_trip_pick_up_time",
                  "two_stuff_needed", "need_oxygen", "need_stretcher", "need_wheel_chair",
                  "have_preferred_driver", "preferred_driver")

    def __init__(self, *args, **kwargs):
        super(CustomerRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['customer_id'].widget = HiddenInput()
        self.fields['customer_id'].required=False
        self.fields['pick_from_institution'].required=False
        self.fields['pick_from_institution'].initial=True
        self.fields['pick_from_institution'].label = 'Pick-up from an Institution?'
        self.fields['pick_from_institution'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle", attrs={'onchange': "toggleInstitutionPickup()"})
        self.fields['pickup_institution'].label = 'Choose a pick-up Institution'
        self.fields['pickup_institution'].queryset = Institution.objects.all()

        self.fields['drop_at_institution'].required=False
        self.fields['drop_at_institution'].label = 'Drop-off at an Institution?'
        self.fields['drop_at_institution'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle", attrs={'onchange': "toggleInstitutionDropoff()"})
        self.fields['pickup_institution'].required=False
        self.fields['dropoff_institution'].required=False
        self.fields['dropoff_institution'].label = 'Choose a drop-off Institution'
        self.fields['dropoff_institution'].queryset = Institution.objects.all()

        self.fields['return_trip'].required=False
        self.fields['return_trip'].label = 'Return trip needed?'
        self.fields['return_trip'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle", attrs={'onchange': "toggleVisibility('return_trip', 'return_trip_pick_up_time')"})
        self.fields['return_trip_pick_up_time'].required=False
        self.fields['return_trip_pick_up_time'].label = 'Return trip pick-up date and time'

        self.fields['have_preferred_driver'].required=False
        self.fields['have_preferred_driver'].label = 'Have a favorite driver?'
        self.fields['have_preferred_driver'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle ", attrs={'onchange': "toggleVisibility('have_preferred_driver', 'preferred_driver')"})
        self.fields['preferred_driver'].required=False
        self.fields['preferred_driver'].label = 'Pick a driver'

        self.fields['elvator_in_home'].required=False
        self.fields['elvator_in_home'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle")
        self.fields['two_stuff_needed'].required=False
        self.fields['two_stuff_needed'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle")
        self.fields['need_oxygen'].required=False
        self.fields['need_oxygen'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle")
        self.fields['need_stretcher'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle")
        self.fields['need_stretcher'].required=False
        self.fields['need_wheel_chair'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success right-aligned-toggle")
        self.fields['need_wheel_chair'].required=False

        self.fields['pick_up_time'].widget = DateTimePickerInput()
        self.fields['return_trip_pick_up_time'].widget = DateTimePickerInput()


class NewCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ("customer_type", "institution_id", "patient_name", "contact_name", "contact_phone")
    
    def __init__(self, *args, **kwargs):
        super(NewCustomerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['customer_type'].label = 'Buisness customer?'
        self.fields['customer_type'].required = False
        # self.fields['customer_type'].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success", attrs={'onchange': "toggleVisibility('customer_type', 'institution_id')"})
        self.fields["customer_type"].widget.attrs.update({'onchange': "toggleVisibility('have_preferred_driver', 'preferred_driver')"})
        self.fields['institution_id'].required = False

    def clean_customer_type(self):
        customer_type = self.cleaned_data['customer_type']
        if customer_type in [0, '0']:
            return False
        elif customer_type in [1, '1']:
            return True
        return customer_type

    def save(self, commit=True):
        instance = super(NewCustomerForm, self).save(commit=False)
        # Ensure customer_type is stored as 0/1
        instance.customer_type = 1 if instance.customer_type else 0

        if commit:
            instance.save()
        return instance


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
		fields = (
            "institution_name",
            "institution_adress",
            "in_institution",
            "status",
            "inst_id"
        )

	def __init__(self, *args, **kwargs):
		instance = kwargs.get('instance')
		super(UpdateInstitutionForm, self).__init__(*args, **kwargs)
		if instance:
			excluded_ids = [instance.pk] + list(instance.children.values_list('pk', flat=True))
			self.fields['in_institution'].queryset = Institution.objects.exclude(pk__in=excluded_ids)
		else:
			self.fields['in_institution'].queryset = Institution.objects.all()
	
	def save(self, commit=True):
		inst = super(UpdateInstitutionForm, self).save(commit=False)
		if commit:
			inst.save()
		return inst


class DateFilterForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))