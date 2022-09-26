from tkinter import Widget
from .models import Ride
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput


#Register your Forms here
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class loginForm(forms.Form):
    username = forms.CharField(max_length = 150, label='')
    password = forms.CharField(max_length = 128, widget = forms.PasswordInput, label='')
    username.widget.attrs['class'] = 'input'
    password.widget.attrs['class'] = 'input'
    username.widget.attrs['placeholder'] = 'Username'
    password.widget.attrs['placeholder'] = 'Password'

class create_rideForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["Source_Address"].label = ""
        self.fields["Source_Address"].widget.attrs["class"] = "input"
        self.fields["Source_Address"].widget.attrs["placeholder"] = "From:"
        self.fields["Dest_Address"].label = ""
        self.fields["Dest_Address"].widget.attrs["class"] = "input"
        self.fields["Dest_Address"].widget.attrs["placeholder"] = "To:"
        self.fields["NumberPlate"].label = ""
        self.fields["NumberPlate"].widget.attrs["class"] = "input"
        self.fields["NumberPlate"].widget.attrs["placeholder"] = "Number Plate"
        self.fields["date"].label = ""
        self.fields["date"].widget.attrs["class"] = "input"
        self.fields["time"].label = ""
        self.fields["time"].widget.attrs["class"] = "input"
        self.fields["Occupancy"].label = ""
        self.fields["Occupancy"].widget.attrs["class"] = "input"
        self.fields["Occupancy"].widget.attrs["placeholder"] = "Occupancy"

    class Meta:
        model = Ride
        fields = ["Source_Address", "Dest_Address", "NumberPlate", "date", "time", "Occupancy", "UserName"]
        widgets = {
            'UserName' : forms.HiddenInput(),
            'date' : DateInput(),
            'time' : TimeInput(),
        }

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "input"
        self.fields["password1"].widget.attrs["class"] = "input"
        self.fields["password2"].widget.attrs["class"] = "input"
        self.fields["username"].widget.attrs["label"] = " "
        self.fields["password1"].widget.attrs["label"] = " "
        self.fields["password2"].widget.attrs["label"] = " "
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Password"
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
        self.fields["username"].label = ""
        self.fields["password1"].label = ""
        self.fields['password2'].label = ""

    class Meta:
        model = User
        fields = ["username", "password1", "password2"] 

