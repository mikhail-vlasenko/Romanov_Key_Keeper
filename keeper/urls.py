from django.urls import path

from . import views

app_name = 'keeper'
urlpatterns = [
    path('', views.index, name='index'),
    path('history/page/<int:page_id>/', views.history, name='history'),
    path('history/', views.history, name='history'),
    path('reg/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('accounts/login/', views.login_user, name='login'),
    # path('login/change_pass/', views.change_pass, name='change_pass'),
    # path('accounts/login/change_pass/', views.change_pass, name='change_pass'),
    path('logout/', views.logout_user, name='logout'),
    path('card/', views.card_take, name='card'),
    path('about/', views.about, name='about'),
]
