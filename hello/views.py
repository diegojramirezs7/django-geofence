from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import generic

from .models import Greeting
from .models import GeofenceEvent, Geofence, LocationUpdate
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
		try:
			request_data = json.loads(request.body.decode("utf-8"))
			geofence = request_data['geofence']
			time = request_data['time']
			event = request_data['event']

			#geofence = request.POST['geofence']
			#time = request.POST['time']
			#event = request.POST['event']

			date_time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
			# "2021-02-10T12:42:55.655"
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

			return JsonResponse({"success": True})
		except Exception as e:
			return JsonResponse({"error": str(e)})

	else:
		ls = []
		events = GeofenceEvent.objects.all().order_by('time')
		for event in events:
			pretty_time = event.time.strftime("%m/%d/%Y, %H:%M:%S")
			ls.append({'geofence': event.geofence.name, 'eventType': event.event, 'time': pretty_time})

		return render(request, 'event_log.html', {'events': ls})




@csrf_exempt
def location(request):
	if request.method == 'POST':
		lat = request.POST['latitude']
		lng = request.POST['longitude']
		time = request.POST['time']

		date_time_obj = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')

		location_object = LocationUpdate(
			latitude = lat,
			longitude = lng, 
			time = time
		)

		location_object.save()

		return HttpResponse("succces")
	else:
		ls = []
		location_updates = LocationUpdate.objects.all().order_by('time')
		for update in location_updates:
			pretty_time = update.time.strftime("%m/%d/%Y, %H:%M:%S")
			ls.append({'lat': update.latitude, 'lng': update.longitude, 'time': update.time})

		return render(request, 'location_updates.html', {'updates': ls})





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
