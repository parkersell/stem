from django.shortcuts import render, redirect

import csv, io
from django.contrib import messages
# Create your views here.
from .models import Syncing, Chart, Student
from django.views.generic.edit import FormView, View
from .forms import DataUpload, SyncUpload, ChartSelect
from django.http import JsonResponse, Http404, HttpResponseRedirect   

from rest_framework.views import APIView
from rest_framework.response import Response

import fitbit
from fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime

print("http://localhost:8000/sync")

class ChartView(View):
    form_class = ChartSelect
    initial ={"str_student": "Parker"}#learn to skip chartselect and just use a default that was saved

    def get(self, request, *args, **kwargs):
        name = self.kwargs['name'] 
        form = self.form_class() #initial=self.initial)
        student = Student.objects.get(student_name=name)
        pk_list = student.pk-1 #because in the json the first number is 0 not 1(like it is for pk)
        return render(request, 'charts_ex.html', {"form": form, "student": pk_list})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            student = form.cleaned_data.get('str_student')
            try:
                student = Student.objects.get(student_name=student)
            except Student.DoesNotExist:
                raise Http404("Student does not exist") 
            #initial = {"str_student":student} #how to store this?
            return redirect('hrchart', name=student)
        return redirect('chartselect')

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, Format=None):
        json =Chart.getallstudents("hour")
        return Response(data=json)

def home(request):
    return render(request, 'home.html')


class DataView(FormView):
    template_name = "data_upload.html"
    form_class = DataUpload
    success_url = "/upload/"

    def form_valid(self, form):
        form.process_hr_data()
        return super().form_valid(form)

def syncpage(request):
    if request.method == 'POST':
        form = SyncUpload(request.POST)
        if form.is_valid():
            Syncing.syncFitbitData(form.cleaned_data.get('sync_date'), form.cleaned_data.get('str_student'))
            return redirect('syncsuccess') 
    else:
        form = SyncUpload()
    return render(request, 'syncpage.html', {'form': form})

def syncsuccess(request):
    return render(request, 'syncsuccess.html')

def chartselect(request):
    if request.method == 'POST':
        form = ChartSelect(request.POST)
        if form.is_valid():
            student = form.cleaned_data.get('str_student')
            return redirect('hrchart', name=student) 
    else:
        form = ChartSelect(initial={"str_student": "Parker"} )
    return render(request, 'chartselect.html', {'form': form})

