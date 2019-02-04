from django.urls import path

from . import views

app_name = 'keeper'
urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('reg/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('card/', views.card_take, name='card'),
    path('transfer/', views.transfer, name='transfer'),
    path('accounts/login/', views.login_user, name='login'),
    path('about/', views.about, name='about'),  # add about page
]
