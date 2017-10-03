from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from trello.forms import *
from trello.models import *
from trello.serializers import CardSerializer


# Create your views here.

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('trello:base')
        return render(request, 'trello/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        user = authenticate(username=username, password=password1)  # checks in database if they are user if they exist

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('trello:base')

        return render(request, 'trello/login.html', {'msg': 'Błędny login lub hasło'})


class SignupView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'trello/singup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        # import pdb; pdb.set_trace()
        if form.is_valid():
            user = form.save(commit=False)

            # cleaned data
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                user.set_password(password1)
                user.save()
                user = authenticate(username=username,
                                    password=password1)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('trello:base')
            return render(request, 'trello/singup.html', {'form': form})



        return render(request, 'trello/singup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('trello:login')



class BaseView(LoginRequiredMixin, View):
    def get(self, request):
        alllist = List.objects.filter(owner=request.user)
        listform = ListForm()
        cardform = CardForm()
        return render(request, "trello/base.html", {'listform': listform, 'alllist': alllist, "cardform": cardform})


class ListCreate(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST["name"]
        owner = request.user
        List.objects.create(owner=owner, name=name)
        return HttpResponse("Jest")


class ListCopy(LoginRequiredMixin, View):
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


class ListDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        list = List.objects.get(pk=int(pk))
        list.delete()
        return HttpResponse("usunieto")


class DeleteAllCards(LoginRequiredMixin, View):
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


class CardCreate(LoginRequiredMixin, View):
    def post(self, request):
        name = request.POST["name"]
        description = request.POST["description"]
        list = List.objects.get(pk=int(request.POST["list"]))
        Card.objects.create(name=name, description=description, list=list)
        return HttpResponse("Jest")


class CardEdit(LoginRequiredMixin, View):
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


class CardDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        card = Card.objects.get(pk=int(pk))
        card.delete()
        return HttpResponse("usunieto")


class CardDetail(LoginRequiredMixin, APIView):
    def get(self, request, pk):
        card = Card.objects.get(pk=int(pk))
        serializer = CardSerializer(card)
        return Response(serializer.data)
