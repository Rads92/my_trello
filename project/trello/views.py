from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from trello.forms import *
from trello.models import *
from trello.serializers import CardSerializer


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


class ListCopy(View):
    def post(self, request, pk):
        # import pdb; pdb.set_trace()
        obj = List.objects.get(pk=int(pk))
        cards = obj.card_set.all()
        obj.pk = None
        obj.save()
        for card in cards:
            card.pk = None
            card.list = obj
            card.save()
        return HttpResponse("Jest")


class ListDelete(View):
    def post(self, request, pk):
        list = List.objects.get(pk=int(pk))
        list.delete()
        return HttpResponse("usunieto")


class DeleteAllCards(View):
    def post(self, request, pk):
        # import pdb; pdb.set_trace()
        listOld = List.objects.get(pk=int(pk))
        for card in listOld.card_set.all():
            if request.POST.get("newlist"):
                new = List.objects.get(pk=int(request.POST.get("newlist")))
                card.list = new
                card.save()
            else:
                card.delete()
        return HttpResponse("")




class CardCreate(View):
    def post(self, request):
        name = request.POST["name"]
        description = request.POST["description"]
        list = List.objects.get(pk=int(request.POST["list"]))
        Card.objects.create(name=name, description=description, list=list)
        return HttpResponse("Jest")


class CardEdit(View):
    def post(self, request, pk):
        # import pdb; pdb.set_trace()
        card = Card.objects.get(pk=int(pk))
        if request.POST.get('name'):
            card.name = request.POST.get('name')
        if request.POST.get('description'):
            card.description = request.POST.get('description')
        if request.POST.get('list'):
            card.list = List.objects.get(pk=int(request.POST['list']))
        card.save()
        return HttpResponse("Edytowano")


class CardDelete(View):
    def post(self, request, pk):
        card = Card.objects.get(pk=int(pk))
        card.delete()
        return HttpResponse("usunieto")


class CardDetail(APIView):
    def get(self, request, pk):
        card = Card.objects.get(pk=int(pk))
        serializer = CardSerializer(card)
        return Response(serializer.data)
