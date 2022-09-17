from django.shortcuts import render, redirect, HttpResponse
from .forms import loginForm, create_rideForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Ride, Request
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
    ride_list = Ride.objects.all()
    context = {'ride_list' : ride_list}
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
        context = {'create_rideForm' : form}
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

def deleteRide(request, rideID):
        Ride.objects.filter(RideID = rideID).delete()
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

def home(request):
    return render(request, 'home.html')

def optOut(request, rideID):
    current_user = request.user.username
    ride = Ride.objects.get(RideID = rideID)
    if current_user == ride.UserName:
        messages.success(request, "Cannot Opt Out of your own ride")
        return redirect("allRides")
    Request.objects.get(RideID = rideID, UserName = current_user).delete()
    return redirect("allRides")

def logout(request):
    return redirect("login")