from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render
from .forms import *


def index(request):
    context = {}
    if request.method == 'POST':
        f = TakeKeyForm(request.POST)
        if f.is_valid():
            if request.user.is_authenticated:
                hist = History(key=f.data['key_num'], time_cr=timezone.now(), user_id=request.user)
                hist.save()
                context['message'] = 'You got a key!'
            else:
                context['message'] = 'Log in first!'

    else:
        f = TakeKeyForm()

    key_list = History.objects.filter(user_id=request.user, active=True)
    context['key_list'] = key_list
    context['form'] = f
    context['user_id'] = request.user
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
            context['message'] = 'U r successfully registered!'
            context['users'] = User.objects.all()
            user = authenticate(request, username=f.data['username'], password=f.data['password'])
            if user is not None:
                login(request, user)

        elif f.data['password'] != f.data['password2']:
            context['message'] = 'passwords do not match'

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
                context['message'] = 'logged in'
                print("logged")
            else:
                context['message'] = 'failed to log in'

    else:
        f = LoginForm()

    context['form'] = f
    return render(request, 'login.html', context)
