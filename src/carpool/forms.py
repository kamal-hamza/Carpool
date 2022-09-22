from .models import Ride
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


#Register your Forms here
class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class loginForm(forms.Form):
    username = forms.CharField(max_length = 150, label='')
    password = forms.CharField(max_length = 128, widget = forms.PasswordInput, label='')
    username.widget.attrs['class'] = 'form-field'
    password.widget.attrs['class'] = 'form-field'

class create_rideForm(ModelForm):
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
        self.fields["username"].widget.attrs["class"] = "form-field"
        self.fields["password1"].widget.attrs["class"] = "form-field"
        self.fields["password2"].widget.attrs["class"] = "form-field"
        self.fields["username"].widget.attrs["label"] = ""
        self.fields["password1"].widget.attrs["label"] = ""
        self.fields["password2"].widget.attrs["label"] = ""

    class Meta:
        model = User
        fields = ["username", "password1", "password2"] 

