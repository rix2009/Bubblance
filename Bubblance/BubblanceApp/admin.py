from django.contrib import admin
from django.apps import apps
from django.db import models


def register_all_app_models():
   models_to_ignore = [
       'admin.LogEntry',
       'contenttypes.ContentType',
       'sessions.Session',
       'authtoken.TokenProxy',
       'authtoken.Token',
       ]
   for model in apps.get_models():
       try:
           if model._meta.label in models_to_ignore:
               continue
           else:
               class modelAdmin(admin.ModelAdmin):  
                   list_display = [field.name for field in model._meta.fields]

               admin.site.register(model, modelAdmin)
       except admin.sites.AlreadyRegistered:
           pass


register_all_app_models() # Call the function after registering any specific model admin class.
