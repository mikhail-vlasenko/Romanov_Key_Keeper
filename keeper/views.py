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
            hist = History(key=f.data['key_num'], time_cr=timezone.now(), user_id='admin')  # put a user, not admin
            hist.save()

    else:
        f = TakeKeyForm()

    context['form'] = f
    return render(request, 'index.html', context)


def history(request):
    hist_list = History.objects.all()
    context = {'hist_list': hist_list}
    return render(request, 'history.html', context)
