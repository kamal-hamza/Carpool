from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.login_user, name = "login"),
    path('signup/', views.signup_user, name = "signup"),
    path('allrides/', views.allRides, name = "allRides"),
    path('create/', views.create_ride, name = "create"),
    path('myrides/', views.myRide, name = "myRides"),
    path('optin/<rideID>', views.optIn, name = "optIn"),
    path('delete/<rideID>', views.deleteRide, name = "delete"),
    path('updateform/<rideID>"', views.updateForm, name = "updateform"),
    path('requestRide/<rideID>', views.requestRide, name = "requestRide"),
    path('approve/<str:Username>/<int:rideID>', views.approve, name = "approve"),
    path('deny/<str:Username>/<int:rideID>', views.deny, name = "deny"),
    path('approvedrides/', views.approvedRides, name = "approvedRides"),
    path('optout/<int:rideID>', views.optOut, name = "optOut"),
    path('', views.home, name = "home"),
    path('logout/', views.logout_user, name = "logout"),
    path('pending', views.pendingRides, name = "pendingRides"),
    path('map/<int:rideID>', views.viewMap ,name = "map"),
]