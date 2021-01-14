from django.db import models

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField("date created", auto_now_add=True)

class GeofenceEvent(models.Model):
	time = models.DateTimeField("recorded", auto_now_add=True)
	event = models.CharField(max_length=255, blank=True)
	user = models.CharField(max_length=255, blank=True, null=True)
	project = models.CharField(max_length=255, blank=True, null=True)

