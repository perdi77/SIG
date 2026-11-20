from django.shortcuts import render
from django.http import HttpResponse
from .view_peta import petasatu, petadua

def welcome(request):
    return HttpResponse("<h1>Selamat Datang di Website GIS UMKM</h1>")

# Create your views here.
