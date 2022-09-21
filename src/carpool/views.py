from django.shortcuts import render, redirect
from .forms import loginForm, create_rideForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Ride, Request
import folium
from geopy.geocoders import Nominatim
import openrouteservice as ors
# Create your views here.

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Successfully Logged In"))
            return redirect('allRides')
        else:
            messages.success(request, ("There was an Error in your form!"))
            return redirect('login')
    else:
        context = {'form' : loginForm()}
        return render(request, 'login.html' ,context)

def signup_user(request):
    if request.method == 'POST':
        form  = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Your account was created successfully"))
            return redirect("login")
        else:
            messages.success(request, ("There was an error validating your form"))
            return redirect("signup")
    else:
        context = {'form' : UserCreationForm()}
        return render(request, 'signup.html', context)

def allRides(request):
    current_user = request.user.username  
    ride_list = Ride.objects.all()
    context = {'ride_list' : ride_list, 'current_user' : current_user}
    return render(request, 'allRides.html', context)


def create_ride(request):
    current_user = request.user.username
    if request.method == "POST":
        form = create_rideForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("Your ride was created successfully"))
            return redirect("myRides")
        else:
            messages.success(request, ("There was an error in your form"))
            return redirect("create")
    else:
        form = create_rideForm(initial = {'UserName' : current_user})
        context = {'create_rideForm' : form, 'map' : map}
        return render(request, 'create.html', context)

def myRide(request):
    current_user = request.user.username
    allRides = Ride.objects.filter(UserName = current_user)
    context = {'allRides' : allRides}
    return render(request, 'myRides.html', context)

def optIn(request, rideID):
    current_user = request.user.username
    ride = Ride.objects.get(RideID = rideID)
    if current_user == ride.UserName:
        messages.success(request, ("Cannot request your own ride."))
        return redirect("allRides")
    else:
        requestRide = Request.objects.get_or_create(RideID = rideID, UserName = current_user)
        messages.success(request, ("Ride Request Successfully"))
        return redirect("allRides")

def optOut(request, rideID):
    current_user = request.user.username
    Request.objects.get(RideID = rideID, UserName = current_user).delete()
    return redirect("allRides")

def deleteRide(request, rideID):
        Ride.objects.filter(RideID = rideID).delete()
        Request.objects.filter(RideID = rideID).delete()  
        return redirect("allRides")

def updateForm(request, rideID):
    ride = Ride.objects.get(RideID = rideID)
    form = create_rideForm(request.POST or None, instance = ride)
    if form.is_valid():
        form.save()
        return redirect("myRides")
    context = {'form' : form}
    return render(request, 'updateRide.html', context)

def requestRide(request, rideID):
    rideRequests = Request.objects.filter(RideID = rideID)
    context = {'rideRequests' : rideRequests}
    return render(request, 'approve.html', context)

def approve(request, Username, rideID):
    requestRide = Request.objects.get(RideID = rideID, UserName = Username)
    requestRide.Approved = True
    requestRide.save()
    ride = Ride.objects.get(RideID = rideID)
    seats = ride.Occupancy
    ride.Occupancy = seats - 1
    ride.save()
    messages.success(request, ("Approved User"))
    return redirect("myRides")

def deny(request, Username, rideID):
    requestRide = Request.objects.get(RideID = rideID, UserName = Username)
    requestRide.delete()
    messages.success(request, ("Denied User"))
    return redirect("myRides")

def approvedRides(request):
    current_user = request.user.username
    approvedRides = []
    rides = Request.objects.filter(UserName = current_user, Approved = True)
    for ride in rides:
        id = ride.RideID
        approvedRides.append(Ride.objects.get(RideID = id))
    context = {'approvedRides' : approvedRides}
    return render(request, 'approvedRides.html', context)

def pendingRides(request):
    current_user = request.user.username
    pendingRides = []
    rides = Request.objects.filter(UserName = current_user, Approved = False)
    for ride in rides:
        id = ride.RideID
        pendingRides.append(Ride.objects.get(RideID = id))
    context = {'pendingRides' : pendingRides}
    return render(request, 'pendingRides.html', context)

def home(request):
    return render(request, 'home.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("Successfully logged out"))
    return redirect("login")

def viewMap(request, rideID):
    map = folium.Map()
    ride = Ride.objects.get(RideID = rideID)
    sourceDest = ride.Source_Address
    destination = ride.Dest_Address
    sourceLoc = Nominatim(user_agent="getSourceLoc")
    destLoc = Nominatim(user_agent="getDestLoc")
    getSourceLoc = sourceLoc.geocode(sourceDest)
    getDestLoc = destLoc.geocode(destination)
    destLat = getDestLoc.latitude
    destLong = getDestLoc.longitude
    sourceLat = getSourceLoc.latitude
    sourceLong = getSourceLoc.longitude
    destList = [destLat, destLong]
    sourceList = [sourceLat, sourceLong]
    map = folium.Map()
    ors_key = '5b3ce3597851110001cf6248c1de9e7c306e4380aceb7860dff10d71'
    client = ors.Client(key=ors_key)
    coords = [[sourceLong, sourceLat], [destLong, destLat]]
    route = client.directions(coordinates = coords, profile = 'driving-car', format = 'geojson')
    folium.GeoJson(route, name='route').add_to(map)
    folium.LayerControl().add_to(map)
    folium.Marker(sourceList).add_to(map)
    folium.Marker(destList).add_to(map)
    map = map._repr_html_()
    context = {'map' : map}
    return render(request, 'map.html', context)

