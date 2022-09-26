from django.db import models
# Create your models here.

class Ride(models.Model):
    RideID = models.AutoField(primary_key = True)
    Source_Address = models.CharField(max_length = 128, help_text="")
    Dest_Address = models.CharField(max_length = 128, help_text="")
    NumberPlate = models.CharField(max_length = 128, help_text="")  
    date = models.DateField(help_text="")
    time = models.TimeField(help_text="")
    Occupancy = models.IntegerField(help_text="")
    UserName = models.CharField(max_length = 128, help_text="")

    def __str__(self):
        return self.Source_Address + " - " + self.Dest_Address

class Request(models.Model):
    RideID = models.IntegerField()
    UserName = models.CharField(max_length = 128)
    Approved = models.BooleanField(default = False)

    def __str__(self):
        return self.UserName