from django.urls import path

from . import views

app_name = 'keeper'
urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('reg/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
]
