from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from trello.forms import *
from trello.models import *


# Create your views here.


class BaseView(View):
    def get(self, request):
        alllist = List.objects.all()
        listform = ListForm()
        cardform = CardForm()
        return render(request, "trello/base.html", {'listform': listform, 'alllist': alllist, "cardform": cardform})


class ListCreate(View):
    def post(self, request):
        name = request.POST["name"]
        List.objects.create(name=name)
        return HttpResponse("Jest")


class CardCreate(View):
    def post(self, request):
        name = request.POST["name"]
        description = request.POST["description"]
        list = List.objects.get(pk=int(request.POST["list"]))
        Card.objects.create(name=name, description=description, list=list)
        return HttpResponse("Jest")
