from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from trello.forms import *
from trello.models import *
from trello.serializers import CardSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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

class CardEdit(View):
    def post(self, request, pk):
        card = Card.objects.get(pk=int(pk))
        card.name = request.POST['name']
        card.description = request.POST['description']
        card.save()
        return HttpResponse("Edytowano")

class CardDelete(View):
    def post(self, request, pk):
        card = Card.objects.get(pk=int(pk))
        card.delete()
        return HttpResponse("usunieto")



class CardDetail(APIView):

    def get(self, request, pk):
        card=Card.objects.get(pk=int(pk))
        serializer = CardSerializer(card)
        return Response(serializer.data)
