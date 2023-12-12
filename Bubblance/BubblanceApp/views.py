from django.shortcuts import render, redirect
from .forms import NewUserForm, NewAmbulanceForm, NewEquipmentForm, EqupmentInAmbulanceForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .models import BUser, Ambulance



# Create your views here.

def index(request):
	context = {}
	context["users"] = BUser.objects.all()
	return render(request, "index.html", context)


def register_request(request):
	form = NewUserForm()
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			messages.success(request, "user added successfuly." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect(reverse("home"), kwargs={"user": user})
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("home")


def create_ambulance(request):
	form = NewAmbulanceForm()
	if request.method == "POST":
		form = NewAmbulanceForm(request.POST)
		if form.is_valid():
			ambulance = form.save()
			messages.success(request, "Ambulance added successfuly." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="create_ambulance.html", context={"create_ambulance_form":form})


def ambulance(request):
	context = {}
	context["ambulance"] = Ambulance.objects.all()
	if request.method == "POST":
		amb = request.POST
		request.session
		render(request=request, template_name="create_eq.html", context = {"amb":amb})
	return render (request=request, template_name="ambulance.html", context = context)


def create_equipment(request):
	amb = request.POST["amb"]
	form1 = NewEquipmentForm()
	form2 = EqupmentInAmbulanceForm()
	if request.method == "POST":
		form1 = NewEquipmentForm(request.POST)
		form2 = EqupmentInAmbulanceForm(request.POST)
		if form1.is_valid() and form2.is_valid():
			eq = form1.save()
			form2.eq_id = eq
			eq_in_ambulance = form2.save()
			messages.success(request, "Equipment added successfuly." )
			return redirect("home")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="create_eq.html", 
				context={"create_equipment_form":form1, "equipment_in_ambulance_form":form2, "amb":amb})