from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from .forms import *
from collections import Counter


def index(request):
    context = {}
    if request.method == 'POST':
        f = TakeKeyForm(request.POST)
        if f.is_valid():
            if request.user.is_authenticated:
                hist = History(key=f.data['key_num'], time_cr=timezone.now(), user_id=request.user.username)  # put a user, not admin
                hist.save()
                context['message'] = 'You got a key!'
            else:
                context['message'] = 'Log in first!'

    else:
        f = TakeKeyForm()

    context['form'] = f
    return render(request, 'index.html', context)


def history(request):
    hist_list = History.objects.all()
    context = {'hist_list': hist_list}
    return render(request, 'history.html', context)


def register(request):
    context = {}
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid() and f.data['password'] == f.data['password2']:
            user = User.objects.create_user(username=f.data['username'], password=f.data['password'])
            user.save()
            context['success'] = True
            context['users'] = User.objects.all()

    else:
        f = RegisterForm()

    context['form'] = f
    return render(request, 'register.html', context)


def login_user(request):
    context = {}
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            user = authenticate(request, username=f.data['username'], password=f.data['password'])
            if user is not None:
                login(request, user)
                context['success'] = True
                print("logged")

    else:
        f = LoginForm()

    context['form'] = f
    return render(request, 'login.html', context)
