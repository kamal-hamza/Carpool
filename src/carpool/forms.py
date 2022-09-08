from .models import Ride
from django import forms
from django.forms import ModelForm


#Register your Forms here
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class loginForm(forms.Form):
    username = forms.CharField(max_length = 150)
    password = forms.CharField(max_length = 128, widget = forms.PasswordInput)

class create_rideForm(ModelForm):
    class Meta:
        model = Ride
        fields = ["Source_Address", "Dest_Address", "NumberPlate", "date", "time", "Occupancy", "UserName"]
        widgets = {
            'UserName' : forms.HiddenInput(),
            'date' : DateInput(),
            'time' : TimeInput(),
        }
    

