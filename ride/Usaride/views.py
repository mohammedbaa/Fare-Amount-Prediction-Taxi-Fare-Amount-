from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import numpy as np
from math import radians, sin, cos, sqrt, atan2
import joblib
from .models import Trip

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c  # Distance in km
    return distance

def calculate_bearing(lon1, lat1, lon2, lat2):
    dlon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    x = sin(dlon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
    bearing = atan2(x, y)
    bearing = np.degrees(bearing)
    bearing = (bearing + 360) % 360
    return bearing

def index(request):
    if request.method == 'POST':
        pickup_lat = float(request.POST.get('pickup_latitude', 0))
        pickup_lon = float(request.POST.get('pickup_longitude', 0))
        dropoff_lat = float(request.POST.get('dropoff_latitude', 0))
        dropoff_lon = float(request.POST.get('dropoff_longitude', 0))
        distance = float(request.POST.get('distance', 0))

        if pickup_lat and pickup_lon and dropoff_lat and dropoff_lon:
            displacement = haversine(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
            bearing = calculate_bearing(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
            
            now = datetime.now()
            day = now.weekday()  # Monday is 0 and Sunday is 6
            hour = now.hour  # 0 to 23
            
            nyc_lat = 40.7128
            nyc_lon = -74.0060
            
            nyc_dist = min(
                haversine(pickup_lat, pickup_lon, nyc_lat, nyc_lon),
                haversine(dropoff_lat, dropoff_lon, nyc_lat, nyc_lon)
            )
            
            scaler = joblib.load('model/standarscaler.pkl')
            model = joblib.load('model/gb_model.pkl')
            
            X = np.array([[displacement, distance, bearing, nyc_dist, day, hour]])
            X_scaled = scaler.transform(X)
            
            fare_amount = model.predict(X_scaled)[0]
            
            trip = Trip.objects.create(
                pickup_latitude=pickup_lat,
                pickup_longitude=pickup_lon,
                dropoff_latitude=dropoff_lat,
                dropoff_longitude=dropoff_lon,
                displacement=displacement,
                distance=distance,
                bearing=bearing,
                nyc_dist=nyc_dist,
                day=day,
                hour=hour
            )
            
            return render(request, 'ride/result.html', {'fare': fare_amount})
        else:
            return JsonResponse({'error': 'Invalid coordinates'}, status=400)
    
    return render(request, 'ride/index.html')

def predict_view(request):
    return render(request, 'ride/index.html')































# def index(request):
#     return render(request,'fare/predict.html')


# def haversine(lon1, lat1, lon2, lat2):
#     R = 6371  
#     dlon = radians(lon2 - lon1)
#     dlat = radians(lat2 - lat1)
#     a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#     distance = R * c
#     return distance

# def calculate_bearing(lon1, lat1, lon2, lat2):
#     dlon = radians(lon2 - lon1)
#     lat1 = radians(lat1)
#     lat2 = radians(lat2)
#     x = sin(dlon) * cos(lat2)
#     y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)
#     bearing = atan2(x, y)
#     bearing = np.degrees(bearing)
#     bearing = (bearing + 360) % 360
#     return bearing


# def load_model(filepath):
#     with open(filepath, 'rb') as file:
#         model = pickle.load(file)
#     return model

# def scale_input(data):
#     scaler=load_model('model/standarscaler.pkl')
#     scaled_data = scaler.transform([data])
#     return scaled_data[0]


# def calculate_fare(request):
#     if request.method == 'POST':
#         pickup_lat = float(request.POST['pickup_lat'])
#         pickup_lng = float(request.POST['pickup_lng'])
#         dropoff_lat = float(request.POST['dropoff_lat'])
#         dropoff_lng = float(request.POST['dropoff_lng'])

#         displacement = haversine(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
#         distance = abs(pickup_lat - dropoff_lat) + abs(pickup_lng - dropoff_lng)
#         bearing = calculate_bearing(pickup_lng, pickup_lat, dropoff_lng, dropoff_lat)
#         nyc_center = (40.7128, -74.0060)  # NYC center coordinates
#         nyc_dist = haversine(pickup_lat, pickup_lng, nyc_center[0], nyc_center[1])

#         day = datetime.now().weekday()
#         hour = datetime.now().hour

#         # Scale the input
#         scaled_data = scale_input([displacement, distance, bearing, nyc_dist, day, hour])

#         # Load the model and predict the fare
#         model = load_model('model/gb_model.pkl')
#         fare = model.predict([scaled_data])[0]

#         return JsonResponse({'fare': fare})
#     return JsonResponse({'error': 'Invalid request'}, status=400)