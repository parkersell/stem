from django.shortcuts import render

import csv, io
from django.contrib import messages
# Create your views here.
from .models import Rec, Day, Chart, Student
from django.views.generic.edit import FormView, View
from .forms import DataUpload
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

import fitbit
from fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime

print("http://localhost:8000/api/chart/data")
def recent(request):
    recent = Rec.objects.all()
    return render(request, 'recent.html', {'recent': recent})

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts_ex.html', {"customers": 10})

""" def get_data(request, *args, **kwargs): # simple json response without rest api
    data = {
        "sales": 100, 
        "customers": 10,
    }
    return JsonResponse(data=data) """

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, Format=None):
        json =Chart.getallstudents()
        
        return Response(data=json)

def day(request):
    day = Day.objects.all()
    return render(request, 'day.html', {'day': day})


def home(request):
    return render(request, 'home.html')


class DataView(FormView):
    template_name = "data_upload.html"
    form_class = DataUpload
    success_url = "/upload/"

    def form_valid(self, form):
        form.process_hr_data()
        return super().form_valid(form)


def hrchart(request):
    return render(request, 'hrchart.html')

def syncdata(request):
    Chart.syncFitbitData("today", "Test")
    return render(request, 'syncdata.html')

