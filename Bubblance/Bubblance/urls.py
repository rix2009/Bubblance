"""
URL configuration for Bubblance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from BubblanceApp import views
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="home"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("create_ambulance", views.create_ambulance, name = "create_ambulance"),
    path("ambulance", views.ambulance, name = "ambulance"),
    path("create_equipment", views.create_equipment, name = "create_equipment_form"),
    path("ambulance_info", views.ambulance_info, name = "ambulance_info"),
    path("drivers", views.drivers, name = "drivers"),
    path("driver_info", views.driver_info, name = "driver_info"),
    path("disable_ambulance", views.disable_ambulance, name = "disable_ambulance"),
    path("edit_crew", views.driver_to_amb, name = "driver_to_amb"),
    path("end_crew_time", views.end_crew_time, name = "end_crew_time"),
    path("disable_driver", views.disable_driver, name = "disable_driver"),
    path("edit_equipment", views.edit_equipment, name = "edit_equipment"),
    path("institutions", views.institutions, name = "institutions"),
    path("customers", views.customers, name = "customers"),
    path("add_institution", views.add_institution, name = "add_institution"),
    path("institution_info", views.institution_info, name = "institution_info"),
    path('plan_a_ride/', views.plan_a_ride, name='plan_a_ride'),
    path('pick_a_driver/<int:request_id>/', views.pick_a_driver, name='pick_a_driver'),
    path('complete_ride/<int:request_id>/<int:driver_id>/', views.complete_ride, name='complete_ride'),
    path('rides/', views.rides, name='rides'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('driver_home/', views.driver_home, name='driver_home'),
    path('ride_details/<int:ride_id>/', views.ride_details, name='ride_details'),
    path('ride/<int:ride_id>/start/', views.start_ride, name='start_ride'),
    path('ride/<int:ride_id>/finish/', views.finish_ride, name='finish_ride'),
    path('customer-ride/', views.customer_ride_page, name='customer_ride_page'),
    path('get_institution_address/<int:institution_id>', views.get_institution_address, name='get_institution_address'),
    path('start_shift/', views.start_shift, name='start_shift'),
    path('finish_shift/', views.finish_shift, name='finish_shift'),

] + debug_toolbar_urls()


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, documents_root=settings.STATIC_ROOT)