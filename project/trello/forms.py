from django import forms
from django.forms import ModelForm
from trello.models import *


class ListForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add list...', 'class': 'form-control'}),
                           label="")

    class Meta:
        model = List
        fields = "__all__"


class CardForm(ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Add card...', 'class': 'form-control'}),
                                  label="")
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Add card's tite...", 'class': 'form-control'}),
                           label="")
    class Meta:
        model = Card
        fields = ["name", "description"]
