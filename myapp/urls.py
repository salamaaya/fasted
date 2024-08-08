from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('locate/', views.locate_user, name='locate'),
    path('increase/', views.increase, name='increase'),
    path('decrease/', views.decrease, name='decrease'),
    path('prev_month/', views.prev_month, name='prev_month'),
    path('next_month/', views.next_month, name='next_month'),
    path('get_date/', views.get_date, name='get_date'),
    path('get_hijri/', views.get_hijri, name='get_hijri'),
    path('reset_cal/', views.reset_cal, name='reset_cal'),
    path('get_prayer/', views.get_prayer, name='get_prayer'),
]