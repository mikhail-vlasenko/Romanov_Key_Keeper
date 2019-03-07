from .models import *
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect


REG_CODE = '12345'  # code to enable registration


@login_required
def index(request):
    """
    Main page rendering function
    Lets users to transfer key to each other

    :param request: request object
    :return: request answer object, contains *HTML* file
    :rtype: :class: `django.http.HttpResponse`
    """
    context = {}
    if request.method == 'POST':
        f = TransferForm(request.POST)
        if 'transfer_req' in request.POST:
            if f.is_valid():
                try:
                    tran_user = CustomUser.objects.filter(username=f.data['username']).get()
                    if tran_user != request.user.username:
                        try:
                            hist2 = History.objects.filter(key=f.data['key_num'], user_id=request.user,
                                                           active='Не сдан').get()
                            hist2.active = 'Ожидает передачи'
                            hist2.save()
                            tran_user.user_tran_last = str(request.user.username)
                            tran_user.key_tran_last = f.data['key_num']
                            tran_user.save()
                            context['message'] = 'Ожидайте подтверждения'
                        except ObjectDoesNotExist:
                            context['message'] = 'У вас нет такого ключа'
                    else:
                        context['message'] = 'Нельзя передать ключ себе'
                except ObjectDoesNotExist:
                    context['message'] = 'Нет такого пользователя'

        elif 'accept' in request.POST:
            user_tran = CustomUser.objects.filter(username=request.user.user_tran_last).get()
            hist2 = History.objects.filter(key=request.user.key_tran_last, user_id=user_tran,
                                           active='Ожидает передачи').get()
            hist2.active = 'Сдан'
            hist2.time_back = datetime.datetime.now()
            hist2.save()
            hist = History(key=request.user.key_tran_last, user_id=request.user, active='Не сдан')
            hist.save()
            request.user.key_tran_last = -1
            request.user.user_tran_last = 'никто'
            request.user.save()
            context['message'] = 'Вы получили ключ'

        elif 'reject' in request.POST:
            user_tran = CustomUser.objects.filter(username=request.user.user_tran_last).get()
            hist2 = History.objects.filter(key=request.user.key_tran_last, user_id=user_tran,
                                           active='Ожидает передачи').get()
            hist2.active = 'Не сдан'
            hist2.save()
            request.user.key_tran_last = -1
            request.user.user_tran_last = 'никто'
            request.user.save()
            context['message'] = 'Вы отказались получать ключ'

    else:
        f = TransferForm()

    key_list = History.objects.filter(user_id=request.user, active='Не сдан')
    context['key_list'] = key_list

    if request.user.key_tran_last != -1:
        context['key_receive'] = request.user.key_tran_last
        context['user_receive'] = request.user.user_tran_last

    context['form'] = f
    context['user_id'] = str(request.user.last_name) + ' ' + str(request.user.first_name)
    return render(request, 'transfer.html', context)


@login_required
def card_take(request):
    """
    Card using page rendering function
    Lets users to take/return keys using their cards

    :param request: request object
    :return: request answer object, contains *HTML* file
    :rtype: :class: `django.http.HttpResponse`
    """
    context = {}
    if request.method == 'POST':
        f = CardForm(request.POST)
        if f.is_valid():
            try:
                card_user = CustomUser.objects.filter(card_id=f.data['card']).get()
                try:
                    hist_unit = History.objects.filter(key=f.data['key_num'], user_id=card_user, active='Не сдан').get()
                    hist_unit.active = 'Сдан'
                    hist_unit.time_back = datetime.datetime.now()
                    hist_unit.save()
                    context['message'] = 'Вы отдали ключ!'
                except ObjectDoesNotExist:
                    hist = History(key=f.data['key_num'], time_cr=timezone.now(), user_id=card_user)
                    hist.active = 'Не сдан'
                    hist.save()
                    context['message'] = 'Пользователь ' + str(card_user.username) + ' взял ключ №' + str(f.data['key_num'])
            except ObjectDoesNotExist:
                context['message'] = 'Нет такой карты'

    else:
        f = CardForm()

    context['form'] = f
    return render(request, 'card_reader.html', context)


def history(request):
    """
    History page rendering function
    Lets users to see history or search through it
    No login required

    :param request: request object
    :return: request answer object, contains *HTML* file
    :rtype: :class: `django.http.HttpResponse`
    """
    context = {}
    hist_list = []
    if request.method == 'POST':
        f = SearchForm(request.POST)
        if f.is_valid():
            hist_list = History.objects.all()[::-1]
            hist_list = hist_list[:100]
            if f.data['key_num'] != '' and f.data['last_name'] != '':
                hist_list = []
                count = 0
                for x in History.objects.all()[::-1]:
                    if x.user_id.last_name == f.data['last_name'] and x.key == int(f.data['key_num']):
                        hist_list.append(x)
                        count += 1
                        if count == 100:
                            break

            elif f.data['key_num'] != '':
                hist_list = History.objects.filter(key=f.data['key_num'])[::-1]
                hist_list = hist_list[:100]
            elif f.data['last_name'] != '':
                hist_list = []
                count = 0
                for x in History.objects.all()[::-1]:
                    if x.user_id.last_name == f.data['last_name']:
                        hist_list.append(x)
                        count += 1
                        if count == 100:
                            break

            if f.data['is_active'] == 'true':
                context['select_active'] = 'true'
                hist_list2 = []
                for x in hist_list:
                    if x.active == 'Не сдан':
                        hist_list2.append(x)
                hist_list = hist_list2[:100]
            elif f.data['is_active'] == 'false':
                context['select_active'] = 'false'
                hist_list2 = []
                for x in hist_list:
                    if x.active == 'Сдан':
                        hist_list2.append(x)
                hist_list = hist_list2[:100]
            elif f.data['is_active'] == 'waiting':
                context['select_active'] = 'waiting'
                hist_list2 = []
                for x in hist_list:
                    if x.active == 'Ожидает передачи':
                        hist_list2.append(x)
                hist_list = hist_list2[:100]
            else:
                context['select_active'] = 'none'

    else:
        hist_list = History.objects.all()[::-1]
        hist_list = hist_list[:100]
        f = SearchForm()

    context['hist_list'] = hist_list
    context['form'] = f
    return render(request, 'history.html', context)


def register(request):
    """
        Register page rendering function
        Lets users to register on the website

        :param request: request object
        :return: request answer object, contains *HTML* file
        :rtype: :class: `django.http.HttpResponse`
    """
    context = {}
    if request.method == 'POST':
        f = RegisterForm(request.POST)
        if f.is_valid() and f.data['password'] == f.data['password2'] and f.data['reg_code'] == REG_CODE:
            try:
                if CustomUser.objects.filter(card_id=f.data['card_id']).exists():
                    context['message'] = 'Такая карта уже есть'
                else:
                    user = CustomUser.objects.create_user(username=f.data['username'], password=f.data['password'],
                                                          card_id=f.data['card_id'], last_name=f.data['last_name'],
                                                          first_name=f.data['first_name'])
                    user.save()
                    context['message'] = 'Вы успешно зарегистрированы!'
                    user = authenticate(request, username=f.data['username'], password=f.data['password'])
                    if user is not None:
                        login(request, user)
                        return HttpResponseRedirect('/')
            except:  #IntegrityError???
                context['message'] = 'Такое имя пользователя уже есть'

        elif f.data['password'] != f.data['password2']:
            context['message'] = 'Пароли не совпадают'
        elif f.data['reg_code'] != REG_CODE:
            context['message'] = 'Код для регистрации не правильный'

    else:
        f = RegisterForm()

    context['users'] = CustomUser.objects.all()
    context['form'] = f
    return render(request, 'register.html', context)


def login_user(request):
    """
        Login page rendering function
        Lets users to login on the website

        :param request: request object
        :return: request answer object, contains *HTML* file
        :rtype: :class: `django.http.HttpResponse`
    """
    context = {}
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            user = authenticate(request, username=f.data['username'], password=f.data['password'])
            if user is not None:
                login(request, user)
                context['message'] = 'Вход выполнен!'
                return HttpResponseRedirect('/')
            else:
                context['message'] = 'Не получилось войти:('

    else:
        f = LoginForm()

    context['form'] = f
    return render(request, 'login.html', context)


def logout_user(request):
    """
        Logout function

        :param request: request object
        :return: Redirect to login page
        :rtype: :class: `django.http.HttpResponseRedirect`
    """
    logout(request)
    return HttpResponseRedirect('/login')


def about(request):
    """
        About page rendering function

        :param request: request object
        :return: request answer object, contains *HTML* file
        :rtype: :class: `django.http.HttpResponse`
    """
    context = {}
    return render(request, '_build/html/doc_index.html', context)
