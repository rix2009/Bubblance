from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import time
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse, path
from datetime import datetime
from .forms import UpdateInstitutionForm, NewUserForm, NewAmbulanceForm, EqupmentInAmbulanceForm, NewCrewForm
from .forms import UpdateUserForm, NewCustomerForm, NewInstitution, CustomerRequestForm
from .models import BUser, Ambulance, EqInAmbulance, AmbulanceCrew, Institution, Customer, CustomerRide, CustomerRequest
from Bubblance.mixins import AjaxFormMixin, FormErrors, RedrectParams
import requests

# Create your views here.

def index(request):
	context = {}
	context["users"] = BUser.objects.filter(status = 1)
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
				if BUser.objects.get(username=user).status == 1:
					login(request, user)
					messages.info(request, f"You are now logged in as {username}.")
					return redirect(reverse("home"), kwargs={"user": user})
				else:
					messages.error(request,"The user is not active.")
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
			return redirect("ambulance")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="create_ambulance.html", context={"create_ambulance_form":form})


def ambulance(request):
	context = {}
	context["no_amb"] = False
	context["ambulances"] = Ambulance.objects.filter(status = 1)
	if context["ambulances"].count() == 0:
		context["no_amb"] = True
	if request.method == "POST":
		amb = request.POST
		render(request=request, template_name="ambulance_info.html", context = {"amb":amb})
	return render (request=request, template_name="ambulance.html", context = context)


def create_equipment(request):
	amb = Ambulance.objects.get(ambulance_id = request.POST.get('amb'))
	to_submit = request.POST["form_status"]
	form = EqupmentInAmbulanceForm()
	if request.method == "POST" and to_submit:
		form = EqupmentInAmbulanceForm(request.POST)
		if form.is_valid():
			eq = form.save()
			messages.success(request, "Equipment added successfuly." )
			return ambulance_info(request)
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="create_eq.html", 
				context={"form":form, "amb":amb,})


def drivers(request):
	context = {}
	context["users"] = BUser.objects.all()
	context["no_user"] = False		
	if context["users"].count() == 0:
		context["no_user"] = True		
	return render (request=request, template_name="drivers.html", context = context)


def ambulance_info(request):
	context = {}
	if request.method == "POST":
		amb = Ambulance.objects.get(ambulance_id = request.POST.get('amb'))
		eq_in_amb = []
		for e in EqInAmbulance.objects.filter(am_id = amb):
			eq_in_amb.append(e)
		no_driver = True
		for d in AmbulanceCrew.objects.filter(ambulance_id = amb.ambulance_id, start_time__lte = datetime.now()):
			if d.end_time == None :
				context["driver"] = BUser.objects.get(username = d.driver_id)
				no_driver = False
		messages.error(request,"The ambulance is not in use")
		context["amb"] = amb
		context["equipment"] = eq_in_amb
		if no_driver:
			context["busers"] = BUser.objects.all()
		context["no_driver"] = no_driver
		context["new_crew_form"] = NewCrewForm
		return render (request, "ambulance_info.html",context)
	return redirect (reverse("ambulance"))


def disable_ambulance(request):
	if request.method == "POST":
		amb = request.POST.get("amb")
		instance = Ambulance.objects.filter(ambulance_id = amb.ambulance_id)
		for crew in AmbulanceCrew.objects.filter(ambulance_id = amb.ambulance_id):
			crew.status = 2
		for eq in EqInAmbulance.objects.filter(am_id = amb.ambulance_id):
			eq.status = 2
		instance.status = 2
		return redirect (reverse("ambulance"))
	return redirect (reverse("ambulance"))


def driver_to_amb(request):
	if request.method == "POST":
		form = NewCrewForm(request.POST)
		if form.is_valid():
			crew = form.save()
			messages.success(request, "Driver added succesfully to the ambulance")
			return render(request=request, template_name="ambulance_info.html", context =
				  {"amb":form.cleaned_data.get("ambulance_id"), "driver":form.cleaned_data.get("driver_id")})
		messages.error(request, "Failed, pls try again with valid info")
	return redirect(reverse("ambulance"))


def end_crew_time(request):
	if request.method == "POST":
		amb = Ambulance.objects.get(ambulance_id=request.POST.get("ambulance_id"))
		user = BUser.objects.get(username=request.POST.get("username"))
		crew = AmbulanceCrew.objects.get(ambulance_id=amb, driver_id=user, end_time=None)
		crew.end_time = datetime.now()
		crew.save()
		return render(request=request, template_name="ambulance_info.html", context = {"amb":amb, "no_driver":True, "new_crew_form":NewCrewForm})
	return redirect(reverse("ambulance"))	


def driver_info(request):
	user = request.POST.get("buser") or request.GET.get("buser")
	buser = get_object_or_404(BUser, username=user)

	if request.method == 'POST' and request.POST.get("save_form") == "True":
		form = UpdateUserForm(request.POST, instance=buser)
		if form.is_valid():
			form.save()
			messages.success(request, "user updated successfuly.")
			return redirect("drivers")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	else:
		form = UpdateUserForm(instance=buser)
	return render (request=request, template_name="driver_info.html", context={"buser":buser, "update_user_form":form, "save_form": True})


def disable_driver(request):
	if request.method == "POST":
		user = request.POST.get("buser")
		instance = BUser.objects.filter(username = user.user.username)
		for crew in AmbulanceCrew.objects.filter(driver_id = user.user.username):
			crew.status = 2
		instance.status = 2
		return redirect (reverse("drivers"))
	return redirect (reverse("drivers"))


def edit_equipment(request):
	if request.method =="POST":
		amb = Ambulance.objects.get(ambulance_id=request.POST.get("amb"))
		for e in EqInAmbulance.objects.filter(am_id = amb.ambulance_id):
			amount = request.POST[str(e.eq_id)]
			if amount == '0':
				e.delete()
			else:
				e.amount = amount
				e.save()
	return ambulance_info(request)


def institutions(request):
	context = {}
	context["inst"] = Institution.objects.all()
	context["no_inst"] = False
	if context["inst"].count() == 0:
		context["no_inst"] = True
	return render (request=request, template_name="institutions.html", context = context)


def customers(request):
	context = {}
	context["customers"] = Customer.objects.all()
	context["no_customer"] = False
	if context["customers"].count() == 0:
		context["no_customer"] = True
	return render (request=request, template_name="customers.html", context = context)


def add_institution(request):
	form = NewInstitution()
	if request.method == "POST":
		form = NewInstitution(request.POST)
		if form.is_valid():
			inst = form.save()
			messages.success(request, "Institution added successfuly." )
			return redirect("institutions")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	return render (request=request, template_name="add_institution.html", context={"add_institution_form":form})


def institution_info(request):
    inst_id = request.POST.get("inst_id") or request.GET.get("inst_id")
    inst = get_object_or_404(Institution, inst_id=inst_id)
    if request.method == 'POST' and request.POST.get("save_form") == "True":
        form = UpdateInstitutionForm(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            messages.success(request, "Institution updated successfully.")
            return redirect("institutions")
        else:
            messages.error(request, "Unsuccessful update. Invalid information.")
    else:
        form = UpdateInstitutionForm(instance=inst)
    
    return render(request, "institution_info.html", {"inst": inst, "update_inst_form": form, "save_form": True})


# def plan_a_ride(request):
#     form1 = NewCustomerForm()
#     form2 = CustomerRequestForm()
    
#     ambulances = Ambulance.objects.filter(status=1)
#     drivers = []
#     for amb in ambulances:
#         crews = AmbulanceCrew.objects.filter(ambulance_id=amb.ambulance_id, end_time__isnull=True)
#         for crew in crews:
#             driver = BUser.objects.get(username=crew.driver_id)
#             drivers.append(driver)
    
#     if request.method == "POST":
#         if "select_driver" in request.POST:
#             selected_driver_id = request.POST.get("selected_driver")
#             customer_request_id = request.POST.get("customer_request_id")
#             selected_driver = BUser.objects.get(id=selected_driver_id)
#             customer_request = CustomerRequest.objects.get(id=customer_request_id)
#             customer = customer_request.customer_id
#             ambulance = Ambulance.objects.get(id=AmbulanceCrew.objects.filter(driver_id=selected_driver.id).first().ambulance_id)
            
#             CustomerRide.objects.create(
#                 customer_id=customer,
#                 Am_id=ambulance,
#                 driver_id=selected_driver,
#                 customer_req=customer_request,
#                 pick_up_location=customer_request.pick_up_location,
#                 drop_of_location=customer_request.drop_of_location,
#                 pick_up_time=customer_request.pick_up_time,
#                 drop_of_time=None,  # This can be updated later
#                 number_of_stuff_needed=customer_request.number_of_stuff_needed if customer_request.two_stuff_needed else 1,
#                 status=1
#             )
#             messages.success(request, "Customer ride successfully created.")
#             return redirect("home")

#         form1 = NewCustomerForm(request.POST)
#         form2 = CustomerRequestForm(request.POST)
#         if form1.is_valid() and form2.is_valid():
#             customer = form1.save()
#             new_request = form2.save(commit=False)
#             new_request.customer_id = customer
#             departure_time = int(time.mktime(new_request.pick_up_time.timetuple()))
#             favorite_driver = new_request.preferred_driver if new_request.have_preferred_driver else None
            
#             best_drivers = find_best_drivers(settings.GOOGLE_MAPS_API_KEY, drivers, new_request, departure_time, favorite_driver)
#             if best_drivers:
#                 new_request.save()
#                 return render(request, 'best_drivers.html', {'best_drivers': best_drivers, 'drive_request': new_request})
#             else:
#                 messages.error(request, "No suitable driver found.")
#                 return redirect("plan_a_ride")
#         messages.error(request, "Unsuccessful Request. Invalid information.")
    
#     return render(request, 'plan_a_ride.html', context={"c_form": form1, "c_r_form": form2, "drivers": drivers})

def plan_a_ride(request):
    if request.method == "POST":
        c_form = NewCustomerForm(request.POST)
        c_r_formset = CustomerRequestForm(request.POST, request.FILES)
        
        if c_form.is_valid() and c_r_formset.is_valid():
            customer_request = c_form.save()
            c_r_formset.instance = customer_request
            c_r_formset.save()
            messages.success(request, 'Ride request created successfully!')
            return redirect('home')
    else:
        c_form = NewCustomerForm()
        c_r_formset = CustomerRequestForm()
    
    context = {
        'c_form': c_form,
        'c_r_formset': c_r_formset
    }
    return render(request, 'plan_a_ride.html', context)


def best_drivers(request, customer_request_id):
    customer_request = get_object_or_404(CustomerRequest, id=customer_request_id)
    
    ambulances = Ambulance.objects.filter(status=1)
    drivers = []
    for amb in ambulances:
        crews = AmbulanceCrew.objects.filter(ambulance_id=amb.ambulance_id, end_time__isnull=True)
        for crew in crews:
            driver = BUser.objects.get(username=crew.driver_id)
            drivers.append(driver)
    
    departure_time = customer_request.pick_up_time.timestamp()

    best_drivers = find_best_drivers(settings.GOOGLE_MAPS_API_KEY, drivers, customer_request, departure_time)
    
    if request.method == "POST":
        selected_driver_id = request.POST.get('selected_driver')
        selected_driver = get_object_or_404(Driver, id=selected_driver_id)
        customer_request.assigned_driver = selected_driver
        customer_request.save()
        messages.success(request, 'Driver assigned successfully!')
        return redirect('home')
    
    context = {
        'customer_request': customer_request,
        'best_drivers': best_drivers,
    }
    
    return render(request, 'best_drivers.html', context)
    

def get_travel_time(api_key, origin, destination, departure_time):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&departure_time={departure_time}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'OK':
        travel_time = data['routes'][0]['legs'][0]['duration']['value']  # duration in seconds
        return travel_time
    else:
        raise Exception(f"Error fetching data from Google Maps API: {data['status']}")


def find_best_drivers(api_key, drivers, new_request, departure_time, favorite_driver=None):
    travel_times = []
    
    for driver in drivers:
        # Check driver's current assignments
        ongoing_drives = CustomerRide.objects.filter(driver=driver, end_time__gt=new_request.pick_up_time).order_by('end_time')
        
        # If there are ongoing drives, get the end time of the last one
        if ongoing_drives.exists():
            last_drive = ongoing_drives.last()
            available_time = last_drive.end_time
        else:
            available_time = datetime.now()
        
        # Calculate time to finish current drive and reach new pick up location
        if available_time > new_request.pick_up_time:
            continue
        
        try:
            travel_time = get_travel_time(api_key, driver.current_location, new_request.pick_up_location, departure_time)
            travel_times.append((driver, travel_time))
        except Exception as e:
            print(f"Error calculating travel time for driver {driver.id}: {e}")
    
    # Sort by travel time
    travel_times.sort(key=lambda x: x[1])

    best_drivers = []
    
    if favorite_driver:
        best_drivers.append(favorite_driver)
        for driver, travel_time in travel_times:
            if driver != favorite_driver:
                best_drivers.append(driver)
                if len(best_drivers) == 2:
                    break
    else:
        best_drivers = [driver for driver, travel_time in travel_times[:2]]

    return best_drivers