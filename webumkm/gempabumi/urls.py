from django.urls import path
from . import views

urlpatterns = [
    path('', views.gempaterkini, name='gempaterkini'),
]
