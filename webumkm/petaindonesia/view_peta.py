from django.shortcuts import render
from django.http import HttpResponse

def petasatu(request):
    return render(request, 'petaindonesia/petasatu.html')

def petadua(request):
    return render(request, 'petaindonesia/petadua.html')
