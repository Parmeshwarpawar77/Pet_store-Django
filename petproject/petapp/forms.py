from .models import Pet
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model =User
        fields = ['username','email','password1','password2']
        
class AddPet(ModelForm):
    class Meta:
        model = Pet
        fields='__all__'