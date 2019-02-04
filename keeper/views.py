from .models import *
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404, render
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


REG_CODE = '12345'  # code to enable registration


@login_required
def index(request):
    context = {}
    if request.method == 'POST':
        f = TakeKeyForm(request.POST)
        if f.is_valid():
            if request.user.is_authenticated:
                print(request.user)
                hist = History(key=f.data['key_num'], time_cr=timezone.now(), user_id=request.user)
                hist.save()
                context['message'] = 'You got a key!'
            else:
                context['message'] = 'Log in first!'

    else:
        f = TakeKeyForm()

    if request.user.is_active:
        key_list = History.objects.filter(user_id=request.user, active=True)
        context['key_list'] = key_list

    context['form'] = f
    context['user_id'] = str(request.user.last_name) + ' ' + str(request.user.first_name)
    return render(request, 'index.html', context)


def card_take(request):
    context = {}
    if request.method == 'POST':
        f = CardForm(request.POST)
        if f.is_valid():
            card_user = 0
            c_exist = True
            try:
                card_user = CustomUser.objects.filter(card_id=f.data['card']).get()
            except ObjectDoesNotExist:
                context['message'] = 'No such card'
                c_exist = False

            if c_exist:
                try:
                    hist_unit = History.objects.filter(key=f.data['key_num'], user_id=card_user, active=True).get()
                    hist_unit.active = False
                    hist_unit.save()
                    context['message'] = 'You gave a key back!'
                except ObjectDoesNotExist:
                    hist = History(key=f.data['key_num'], time_cr=timezone.now(), user_id=card_user)
                    hist.save()
                    context['message'] = 'You got a key!'

            else:
                context['message'] = 'No such card'

    else:
        f = CardForm()

    context['form'] = f
    return render(request, 'card_reader.html', context)


@login_required
def transfer(request):
    context = {}
    if request.method == 'POST':
        f = TransferForm(request.POST)
        if f.is_valid():
            try:
                tran_user = CustomUser.objects.filter(username=f.data['username']).get()
                try:
                    hist2 = History.objects.filter(key=f.data['key_num'], user_id=request.user, active=True).get()
                    hist2.active = False
                    hist2.save()
                    hist = History(key=f.data['key_num'], time_cr=timezone.now(), user_id=tran_user)
                    hist.save()
                    context['message'] = 'Вы передали ключ!'
                except ObjectDoesNotExist:
                    context['message'] = 'У вас нет такого ключа'
            except ObjectDoesNotExist:
                context['message'] = 'Нет такого пользователя'

    else:
        f = TransferForm()

    if request.user.is_active:
        key_list = History.objects.filter(user_id=request.user, active=True)
        context['key_list'] = key_list

    context['form'] = f
    context['user_id'] = str(request.user.last_name) + ' ' + str(request.user.first_name)
    return render(request, 'transfer.html', context)


def history(request):
    hist_list = History.objects.order_by('time_cr')[::-1]
    context = {'hist_list': hist_list}
    return render(request, 'history.html', context)


def register(request):
    context = {}
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid() and f.data['password'] == f.data['password2'] and f.data['reg_code'] == REG_CODE:
            user = CustomUser.objects.create_user(
                username=f.data['username'], password=f.data['password'],
                card_id=f.data['card_id'], last_name=f.data['last_name'], first_name=f.data['first_name'])
            user.save()
            context['message'] = 'U r successfully registered!'
            context['users'] = CustomUser.objects.all()
            user = authenticate(request, username=f.data['username'], password=f.data['password'])
            if user is not None:
                login(request, user)

        elif f.data['password'] != f.data['password2']:
            context['message'] = 'passwords do not match'
        elif f.data['reg_code'] == REG_CODE:
            context['message'] = 'code is incorrect'

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
                context['user_id'] = str(user.last_name) + ' ' + str(user.first_name)
                key_list = History.objects.filter(user_id=user, active=True)
                context['key_list'] = key_list
                context['form'] = TakeKeyForm()
                return render(request, 'index.html', context)
            else:
                context['message'] = 'failed to log in'

    else:
        f = LoginForm()

    context['form'] = f
    return render(request, 'login.html', context)


def about(request):
    context = {}
    return render(request, 'about.html', context)
