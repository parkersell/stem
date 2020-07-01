from django.shortcuts import render

import csv, io
from django.contrib import messages
# Create your views here.
from .models import Syncing, Day, Chart, Student
from django.views.generic.edit import FormView, View
from .forms import DataUpload, SyncUpload
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

import fitbit
from fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime

print("http://localhost:8000/sync/success")
def recent(request):
    recent = Syncing.objects.all()
    return render(request, 'recent.html', {'recent': recent})

class ChartView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts_ex.html', {"student": 3})# pk of student

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
        json =Chart.getallstudents("hour")
        
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

class SyncView(FormView):
    template_name = "syncpage.html"
    form_class = SyncUpload
    success_url= "/sync/success"
    def form_valid(self, form):
        """ form.syncstudent("today")
        return super().form_valid(form) """
        return HttpResponse("Sweeeeeet.")


def hrchart(request):
    return render(request, 'hrchart.html')

def syncsuccess(request):
    Syncing.syncFitbitData("today", "Test")
    return render(request, 'syncsuccess.html')

def syncpage(request):
    students = Student.objects.all()
    return render(request, 'syncsuccess.html',{"students", students})
