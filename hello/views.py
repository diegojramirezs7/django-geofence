from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic

from .models import Greeting
from .models import GeofenceEvent, Geofence
import requests
import json
from datetime import datetime

# Create your views here.
@csrf_exempt
def index(request):
	if request.method == 'GET':
		dc = {}
		ls = []
		geofences = Geofence.objects.all()

		for geofence in geofences:
			ls.append({'name': geofence.name, 'latitude': geofence.lat, 
				'longitude': geofence.lng, 'radius': geofence.radius})
		
		return render(request, 'main.html', {'geofences': ls})
		
	elif request.method == 'POST':
		try:
			name = request.POST['name']
			lat = request.POST['lat']
			lng = request.POST['lng']
			radius = request.POST['radius']

			gf = Geofence(
				name = name,
				lat = lat, 
				lng = lng,
				radius = radius
			)

			gf.save()

			ls = []
			geofences = Geofence.objects.all()

			for geofence in geofences:
				ls.append({'name': geofence.name, 'latitude': geofence.lat, 
					'longitude': geofence.lng, 'radius': geofence.radius})
			
			return render(request, 'main.html', {'geofences': ls})

		except Exception as e:
			return HttpResponse(str(e))
		


@csrf_exempt
def events(request):
	if request.method == 'POST':
		event = request.POST['event']
		geofence = request.POST['geofence']
		time = request.POST['time']

		date_time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
		geofence_queryset = Geofence.objects.all()

		geofence_object = get_object_or_404(Geofence, pk = geofence)

		json_data = {
			'event': event,
			'geofence': str(geofence_object), 
			'time': str(date_time_obj)
		}

		event = GeofenceEvent(
			time = date_time_obj,
			event = event,
			geofence = geofence_object
		)

		event.save()

		return HttpResponse("your data was {}".format(json_data))
	else:
		ls = []
		events = GeofenceEvent.objects.all()
		for event in events:
			pretty_time = event.time.strftime("%m/%d/%Y, %H:%M:%S")
			ls.append({'geofence': event.geofence.name, 'eventType': event.event, 'time': pretty_time})

		return render(request, 'event_log.html', {'events': ls})


@csrf_exempt
def geofences(request):
	if request.method == 'GET':
		ls = []
		geofences = Geofence.objects.all()[:10]
		for geofence in geofences:
			ls.append(
				{
					'name': geofence.name,
					'lat': geofence.lat,
					'lng': geofence.lng,
					'radius': geofence.radius,
					'id': geofence.id
				}
			)

		return JsonResponse(ls, safe=False)


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
