from django.contrib import admin
from .models import Geofence, GeofenceEvent

# Register your models here.
admin.site.register(Geofence)
admin.site.register(GeofenceEvent)