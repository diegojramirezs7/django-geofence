from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)


class Geofence(models.Model):
	lat = models.FloatField()
	lng = models.FloatField()
	name = models.CharField(max_length=255, blank=True, null=True)
	radius = models.IntegerField()


class GeofenceEvent(models.Model):
	time = models.DateTimeField("recorded")
	event = models.CharField(max_length=255, blank=True)
	geofence = models.ForeignKey(Geofence, on_delete=models.CASCADE, related_name='events', null=True)

class LocationUpdate(models.Model):
	latitude = models.FloatField()
	longitude = models.FloatField()
	time = models.DateTimeField("recorded")