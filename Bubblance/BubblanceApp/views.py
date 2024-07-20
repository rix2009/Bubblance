from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from collections import defaultdict
from django.utils import timezone
import time
import win32com.client
import pythoncom
import os
from reportlab.lib import colors, pagesizes
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import pytz
import logging
import pandas as pd
from io import BytesIO
from openpyxl import load_workbook
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.generic.edit import FormView, CreateView
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.urls import reverse, path
from datetime import datetime, timedelta, date
from .forms import UpdateInstitutionForm, NewUserForm, NewAmbulanceForm, EqupmentInAmbulanceForm, NewCrewForm
from .forms import UpdateUserForm, NewCustomerForm, NewInstitution, CustomerRequestForm, DateFilterForm
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
			return redirect("drivers")
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


def get_travel_time(api_key, origin, destination, departure_time):
    israel_tz = pytz.timezone('Asia/Jerusalem')
    reference_time = datetime.now(israel_tz)
    
    if departure_time.tzinfo is None:
        departure_time = israel_tz.localize(departure_time)
    
    if departure_time <= reference_time:
        departure_time = reference_time + timedelta(minutes=5)

    unix_time = int(departure_time.timestamp())
    
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&departure_time={unix_time}&key={api_key}"
    
    logging.info(f"API Request URL: {url}")
    
    response = requests.get(url)
    data = response.json()
    
    logging.info(f"API Response: {data}")
    
    if data['status'] == 'OK':
        travel_time = data['routes'][0]['legs'][0]['duration']['value']
        return travel_time
    else:
        error_message = f"Error fetching data from Google Maps API: {data['status']}"
        if 'error_message' in data:
            error_message += f" - {data['error_message']}"
        logging.error(error_message)
        raise Exception(error_message)


def get_active_drivers():
	ambulances = Ambulance.objects.filter(status=1)
	drivers = []
	for amb in ambulances:
		crews = AmbulanceCrew.objects.filter(ambulance_id=amb.ambulance_id, end_time__isnull=True)
		for crew in crews:
			driver = BUser.objects.get(username=crew.driver_id)
			drivers.append(driver)
	return drivers
	
def get_active_rides_by_driver():
    # Get all active drivers
    drivers = get_active_drivers()
    
    # Initialize a dictionary to store rides by driver
    driver_rides = defaultdict(list)
    
    # Get all active rides and sort them by drop_off_time
    active_rides = CustomerRide.objects.filter(status=1).order_by('drop_of_time')
    
    # Iterate over the active rides and categorize them by driver
    for ride in active_rides:
        driver = ride.driver_id
        if driver in drivers:
            ride_info = {
                'origin': ride.pick_up_location,
                'destination': ride.drop_of_location,
                'start_time': ride.pick_up_time,
                'finish_time': ride.drop_of_time
            }
            driver_rides[driver].append(ride_info)

    return driver_rides


def get_best_drivers_for_request(customer_request, api_key):
    print("Looking for best drivers")
    preferred_driver = None
    best_drivers = []

    if customer_request.have_preferred_driver and customer_request.preferred_driver:
        preferred_driver = customer_request.preferred_driver

    active_drivers_rides = get_active_rides_by_driver()
    active_drivers = get_active_drivers()

    available_drivers = []
    for driver in active_drivers:
        rides = active_drivers_rides.get(driver, [])
        can_fit_ride = True
        driver_arrival_time = None

        start_location = driver.current_location or "hasharon hospital"
        
        if not rides:
            travel_time = get_travel_time(
                api_key,
                start_location,
                customer_request.pick_up_location,
                customer_request.pick_up_time
            )
            driver_arrival_time = customer_request.pick_up_time + timedelta(seconds=travel_time)
        else:
            for i, ride in enumerate(rides):
                if i == 0:
                    travel_time = get_travel_time(
                        api_key,
                        start_location,
                        customer_request.pick_up_location,
                        customer_request.pick_up_time
                    )
                    new_ride_finish = customer_request.pick_up_time + timedelta(seconds=travel_time)
                    if new_ride_finish > ride['start_time']:
                        can_fit_ride = False
                        break
                    driver_arrival_time = customer_request.pick_up_time + timedelta(seconds=travel_time)
                else:
                    prev_ride = rides[i-1]
                    travel_time = get_travel_time(
                        api_key,
                        prev_ride['destination'],
                        customer_request.pick_up_location,
                        prev_ride['finish_time']
                    )
                    new_ride_finish = prev_ride['finish_time'] + timedelta(seconds=travel_time)
                    if new_ride_finish > ride['start_time']:
                        can_fit_ride = False
                        break
                    driver_arrival_time = prev_ride['finish_time'] + timedelta(seconds=travel_time)

        if can_fit_ride:
            available_drivers.append((driver, driver_arrival_time))

    available_drivers.sort(key=lambda x: x[1])

    if preferred_driver:
        preferred_driver_arrival_time = get_travel_time(
            api_key,
            preferred_driver.current_location,
            customer_request.pick_up_location,
            customer_request.pick_up_time
        )
        preferred_driver_arrival_time = customer_request.pick_up_time + timedelta(seconds=preferred_driver_arrival_time)
        best_drivers = [(preferred_driver, preferred_driver_arrival_time)] + available_drivers
    else:
        best_drivers = available_drivers

    return best_drivers


def plan_a_ride(request):
    if request.method == 'POST':
        c_form = NewCustomerForm(request.POST)
        c_r_form = CustomerRequestForm(request.POST)
        
        if c_form.is_valid() and c_r_form.is_valid():
            new_customer = c_form.save()
            new_customer_request = c_r_form.save(commit=False)
            new_customer_request.customer_id = new_customer
            new_customer_request.save()
            print(f"Redirecting to pick_a_driver with request_id: {new_customer_request.id}")
            return redirect('pick_a_driver', request_id=new_customer_request.id)
        else:
            print("Form is not valid")
            print(c_form.errors)
            print(c_r_form.errors)
    else:
        c_form = NewCustomerForm()
        c_r_form = CustomerRequestForm()
    
    return render(request, 'plan_a_ride.html', {'c_form': c_form, 'c_r_form': c_r_form})

def pick_a_driver(request, request_id):
    customer_request = get_object_or_404(CustomerRequest, pk=request_id)
    api_key = settings.GOOGLE_API_KEY
    best_drivers = get_best_drivers_for_request(customer_request, api_key)
    
    context = {
        'customer_request': customer_request,
        'best_drivers': best_drivers,
    }
    return render(request, 'pick_a_driver.html', context)


def complete_ride(request, request_id, driver_id):
    customer_request = get_object_or_404(CustomerRequest, pk=request_id)
    driver = get_object_or_404(BUser, pk=driver_id)
    
    crew = AmbulanceCrew.objects.filter(driver_id=driver, end_time__isnull=True).first()
    ambulance = crew.ambulance_id
    
    pick_up_time = customer_request.pick_up_time
    travel_time = get_travel_time(settings.GOOGLE_API_KEY, customer_request.pick_up_location, customer_request.drop_of_location, pick_up_time)
    drop_of_time = pick_up_time + timedelta(seconds=travel_time)
    
    CustomerRide.objects.create(
        customer_id=customer_request.customer_id,
        Am_id=ambulance,
        driver_id=driver,
        customer_req=customer_request,
        pick_up_location=customer_request.pick_up_location,
        drop_of_location=customer_request.drop_of_location,
        pick_up_time=pick_up_time,
        drop_of_time=drop_of_time,
        number_of_stuff_needed=customer_request.two_stuff_needed + 1,
        status=1,
    )
    
    return redirect('home')



def rides(request):
    ride_type = request.GET.get('type', 'current')
    filter_date = request.GET.get('date')

    form = DateFilterForm(initial={'date': filter_date or datetime.now().date()})

    if filter_date:
        filter_date = datetime.strptime(filter_date, '%Y-%m-%d').date()
    else:
        filter_date = datetime.now().date()

    if ride_type == 'current':
        rides = CustomerRide.objects.filter(status=3)
    elif ride_type == 'scheduled':
        rides = CustomerRide.objects.filter(status=1, pick_up_time__date=filter_date)
    else:  # completed
        rides = CustomerRide.objects.filter(status=2, pick_up_time__date=filter_date)
    
    columns = ['Driver', 'Patient Name', 'Request Pick Up Time', 'Ride Pick Up Time']
    if ride_type == 'current':
        columns.append('Actions')
    elif ride_type == 'scheduled':
        columns[3] = 'Pick Up Location'
    
    context = {
        'rides': rides,
        'columns': columns,
        'ride_type': ride_type,
        'filter_date': filter_date,
        'form': form,
    }
    return render(request, 'rides.html', context)



def generate_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        export_format = request.POST.get('export_format')
        today = date.today().strftime("%d-%m-%Y")
        filename = f"ride report {today}.xlsx"

        # Query rides based on report type and date range
        rides = CustomerRide.objects.filter(pick_up_time__range=[from_date, to_date])
        if report_type == 'private':
            rides = rides.filter(customer_id__customer_type='private')
        elif report_type == 'business':
            rides = rides.filter(customer_id__customer_type='business')
        # Load the template
        template_path = os.path.join(settings.BASE_DIR, 'BubblanceApp/static/report_template.xlsx')
        workbook = load_workbook(template_path)
        sheet = workbook.active
        for index, ride in enumerate(rides, start=2):
            sheet.cell(row=index, column=1, value=ride.pick_up_time.date())
            sheet.cell(row=index, column=2, value=ride.customer_id.institution_id.in_institution.institution_name if ride.customer_id.institution_id and ride.customer_id.institution_id.in_institution else '')
            sheet.cell(row=index, column=3, value=ride.customer_id.institution_id.institution_name if ride.customer_id.institution_id else '')
            sheet.cell(row=index, column=4, value=ride.customer_id.patient_name)
            sheet.cell(row=index, column=5, value=ride.pick_up_location)
            sheet.cell(row=index, column=6, value=ride.drop_of_location)
        temp_excel_path = os.path.join(settings.TEMP_DIR, f"temp_report_{today}.xlsx")
        workbook.save(temp_excel_path)

        if export_format == 'excel':
            with open(temp_excel_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
        elif export_format == 'pdf':
            pythoncom.CoInitialize()
            # Convert Excel to PDF
            excel = win32com.client.Dispatch("Excel.Application")
            wb = excel.Workbooks.Open(temp_excel_path)
            temp_pdf_path = os.path.join(settings.TEMP_DIR, f"temp_report_{today}.pdf")
            wb.SaveAs(temp_pdf_path, FileFormat=57)  # 57 is the code for PDF
            wb.Close()
            excel.Quit()
            pythoncom.CoUninitialize()
   
            with open(temp_pdf_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{filename.replace(".xlsx", ".pdf")}"'

        # Clean up temporary files
        os.remove(temp_excel_path)
        if export_format == 'pdf':
            os.remove(temp_pdf_path)

        return response

    return render(request, 'generate_report.html')


def driver_home(request):
    if request.session.pop('navigation_initiated', False):
        # Clear the session variable and redirect to driver home
        return redirect(reverse('driver_home'))
    driver = request.user.buser
    page_type = request.GET.get('type', 'todo')
    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date = datetime.now().date()

    ongoing_ride = CustomerRide.objects.filter(driver_id=driver, status=3).first()

    if page_type == 'todo':
        active_rides = CustomerRide.objects.filter(driver_id=driver, status=1, pick_up_time__date=selected_date)
    else:
        finished_rides = CustomerRide.objects.filter(driver_id=driver, status=2, pick_up_time__date=selected_date)

    context = {
        'ongoing_ride': ongoing_ride,
        'rides': active_rides if page_type == 'todo' else finished_rides,
        'page_type': page_type,
        'selected_date': selected_date
    }
    return render(request, 'driver_home.html', context)


def ride_details(request, ride_id):
    ride = get_object_or_404(CustomerRide, cust_ride_id=ride_id)
    is_manager = False
    if request.user.buser.usertype == 2:
        is_manager = True 

    customer_link = None
    if is_manager:
        customer_link = request.build_absolute_uri(reverse('customer_ride_page'))
        customer_link += f'?token={ride.token}'  # You'll need to implement this method

    context = {
        'ride': ride,
        'is_manager': is_manager,
        'customer_link': customer_link,
    }
    return render(request, 'ride_details.html', context)


def start_ride(request, ride_id):
    ride = get_object_or_404(CustomerRide, cust_ride_id=ride_id)
    ride.status = 3  # Set status to ongoing
    ride.save()
    
    request.session['navigation_initiated'] = True
    
    navigation_url = f"https://www.google.com/maps/dir/?api=1&destination={ride.pick_up_location}"
    return HttpResponseRedirect(navigation_url)


def finish_ride(request, ride_id):
    ride = get_object_or_404(CustomerRide, cust_ride_id=ride_id)
    ride.status = 2  # Set status to deactive
    ride.save()
    return redirect(reverse('driver_home'))


def customer_ride_page(request):
    token = request.GET.get('token')
    ride = get_object_or_404(CustomerRide, token=token)
    
    context = {
        'ride': ride,
    }
    return render(request, 'customer_ride.html', context)