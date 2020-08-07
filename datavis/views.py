from django.shortcuts import render, redirect

import csv, io
from django.contrib import messages
# Create your views here.
from .models import Syncing, Chart, Student
from django.views.generic.edit import FormView, View
from .forms import DataUpload, SyncUpload, SingleChartSelect, MultiChartSelect
from django.http import JsonResponse, Http404, HttpResponseRedirect   
from django.urls import reverse
from urllib.parse import urlencode

from rest_framework.views import APIView
from rest_framework.response import Response

import fitbit
from fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime

print("http://localhost:8000/multichartselect")

class SingleChartView(View):
    form_class = SingleChartSelect
    initial ={"str_student": "Parker"}#TODO learn to skip chartselect and just use a default that was saved

    def get(self, request, *args, **kwargs):
        name = self.kwargs['name']  
        form = self.form_class() #initial=self.initial)
        student = Student.objects.get(student_name=name)
        pk_list = student.pk-1 #because in the json the first number is 0 not 1(like it is for pk)
        return render(request, 'single_chart.html', {"form": form, "student": pk_list})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            student = form.cleaned_data.get('str_student')
            try:
                student = Student.objects.get(student_name=student)
            except Student.DoesNotExist:
                raise Http404("Student does not exist") 
            #initial = {"str_student":student} #how to store this?
            return redirect('singlechart', name=student)
        return redirect('singlechartselect')

class MultiChartView(View): #TODO I need to create a new rest api endpoint to access multi chart data
    form_class = MultiChartSelect
    initial ={"student_one": "Parker", "student_two": "Test"}#learn to skip chartselect and just use a default that was saved
    student_one = "None"
    student_two = "None"
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        student_one = request.GET.get('student_one')
        student_two = request.GET.get('student_two')
        return render(request, 'multi_chart.html', {"form": form, "student_one": student_one, "student_two": student_two})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            student_one = Student.returnObject(form.cleaned_data.get('student_one'))
            student_two = Student.returnObject(form.cleaned_data.get('student_two'))
            start_time = Chart.returnTime(form.cleaned_data.get('start_time'), student_one)# technically should probably check if both have the time 
            end_time = Chart.returnTime(form.cleaned_data.get('end_time'), student_one)
            if 'DNE' in (student_one, student_one, start_time, end_time):
                if 'DNE' in (start_time, end_time):
                    raise Http404("Time does not exist")
                else:
                    raise Http404("Student does not exist")
            pk_list1 = student_one.pk-1 #because in the json the first number is 0 not 1(like it is for pk)
            pk_list2 = student_two.pk-1
            base_url = reverse('multichart')
            pk_list1url =  urlencode({'student_one': pk_list1})  
            pk_list2url =  urlencode({'student_two': pk_list2}) 
            url = '{}?{}&{}'.format(base_url, pk_list1url, pk_list2url)
            return redirect(url)
        return render(request, 'multichart.html', {"form": form})

class ChartData(APIView):
    authentication_classes = [] 
    permission_classes = []
    def get(self, request, Format=None):
        json =Chart.getallstudents("hour")#this is how I access the data 
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

def singlechartselect(request):
    if request.method == 'POST':
        form = SingleChartSelect(request.POST)
        if form.is_valid():
            student = form.cleaned_data.get('str_student')
            start_time= form.cleaned_data.get('start_time')
            end_time= form.cleaned_data.get('end_time')
           
            return redirect('singlechart', name=student) 
    else:
        form = SingleChartSelect(initial={"str_student": "Parker"} )
    return render(request, 'single_chartselect.html', {'form': form})


def v404(request):
    return render(request, '404.html')

