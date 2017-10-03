from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from trello.models import *


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username...', 'class': 'form-control'}),
                           label="")
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'E-mail...', 'class': 'form-control'}),
                           label="")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password...', 'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password...', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class ListForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add list...', 'class': 'form-control'}),
                           label="")

    class Meta:
        model = List
        fields = ["name"]

class CardForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add card...', 'class': 'form-control'}),
                                  label="")
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Add card's tite...", 'class': 'form-control'}),
                           label="")
    class Meta:
        model = Card
        fields = ["name", "description"]
