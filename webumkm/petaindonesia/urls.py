from django.urls import path
from . import views

urlpatterns = [
    path('', views.petasatu, name='home'),
    path('welcome/', views.welcome, name='welcome'),
    path('petasatu/', views.petasatu, name='petasatu'),
    path('petadua/', views.petadua, name='petadua'),
]
