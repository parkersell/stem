from django.shortcuts import render, redirect

import csv, io
from django.contrib import messages
# Create your views here.
from .models import Syncing, Chart, Student
from django.views.generic.edit import FormView, View
from .forms import DataUpload, SyncUpload, SingleChartSelect, MultiChartSelect
from django.http import JsonResponse, Http404, HttpResponseRedirect   
from django.shortcuts import get_object_or_404, get_list_or_404
from django.urls import reverse
from urllib.parse import urlencode

from rest_framework.views import APIView
from rest_framework.response import Response

import fitbit
from fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd 
from datetime import datetime

print("http://localhost:8000/singlechart")

class SingleChartView(View):
    form_class = SingleChartSelect
    initial ={"student_str": "Parker", "start_time": "DefaultHour", "end_time": "DefaultHour"}
    template = 'single_chart.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        student = request.GET.get('student')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        if 'DefaultHour' == start_time and 'DefaultHour' == end_time:
            datatype = "hour"
        else:
            datatype = "range"
        return render(request, self.template, {"form": form, "student": student, 'start_time': start_time, 'end_time': end_time, "datatype": datatype})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            str_start = form.cleaned_data.get('start_time')
            str_end = form.cleaned_data.get('end_time')
            student, dne = Student.returnObject(form.cleaned_data.get('student_str'))
            if 'DNE' in dne:
                raise Http404("Student does not exist")
            if 'DefaultHour' == str_start and 'DefaultHour' == str_end:
                pass
            else:
                dneStart = Chart.checkTime(str_start)# technically should probably check if both have the time 
                dneEnd = Chart.checkTime(str_end)
                if 'DNE' in (dneStart, dneEnd):
                    raise Http404("Time does not exist")
            pk_list1 = student.pk-1 #because in the json the first number is 0 not 1(like it is for pk)
            base_url = reverse('singlechart')
            pk_list1url =  urlencode({'student': pk_list1})
            start_timeurl =  urlencode({'start_time': str_start})  
            end_timeurl =  urlencode({'end_time': str_end})  
            url = '{}?{}&{}&{}'.format(base_url, pk_list1url, start_timeurl, end_timeurl)
            return redirect(url)
        return render(request, self.template, {"form": form})

class MultiChartView(View): #TODO I need to create a new rest api endpoint and model function to access specific time data
    form_class = MultiChartSelect
    initial ={"student_one": "Parker", "student_two": "Pminus", "start_time": "DefaultHour", "end_time": "DefaultHour"}#learn to skip chartselect and just use a default that was saved
    template = 'multi_chart.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        student_one = request.GET.get('student_one')
        student_two = request.GET.get('student_two')
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        if 'DefaultHour' == start_time and 'DefaultHour' == end_time:
            datatype = "hour"
        else:
            datatype = "range"
        return render(request, self.template, {"form": form, "student_one": student_one, "student_two": student_two, 'start_time': start_time, 'end_time': end_time, 'datatype':datatype})
    
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            str_start = form.cleaned_data.get('start_time')
            str_end = form.cleaned_data.get('end_time')
            student_one, dne1 = Student.returnObject(form.cleaned_data.get('student_one'))
            student_two, dne2 = Student.returnObject(form.cleaned_data.get('student_two'))
            if 'DNE' in (dne1, dne2):
                raise Http404("Student does not exist") 
            if 'DefaultHour' == str_start and 'DefaultHour' == str_end:
                pass
            else:
                dneStart = Chart.checkTime(str_start)# technically should probably check if both have the time 
                dneEnd = Chart.checkTime(str_end)
                if 'DNE' in (dneStart, dneEnd):
                    raise Http404("Time does not exist")
            pk_list1 = student_one.pk-1 #because in the json the first number is 0 not 1(like it is for pk)
            pk_list2 = student_two.pk-1
            base_url = reverse('multichart')
            pk_list1url =  urlencode({'student_one': pk_list1})  
            pk_list2url =  urlencode({'student_two': pk_list2})
            start_timeurl =  urlencode({'start_time': str_start})  
            end_timeurl =  urlencode({'end_time': str_end})  
            url = '{}?{}&{}&{}&{}'.format(base_url, pk_list1url, pk_list2url, start_timeurl, end_timeurl)
            return redirect(url)
        return render(request, self.template, {"form": form})

class ChartData(APIView):
    authentication_classes = [] 
    permission_classes = []
    def get(self, request, Format=None):
        start_time = request.GET.get('start_time')
        end_time = request.GET.get('end_time')
        datatype = request.GET.get('datatype')
        if datatype == "hour":
            json =Chart.getallstudents("hour")
        elif datatype == "range":
            start_time = Chart.jqueryToDatetime(start_time)
            end_time = Chart.jqueryToDatetime(end_time)
            start_times = get_list_or_404(Chart, time=start_time)#could check the length to make sure both students have it or something. Mainly using this to avoid the MultipleObjectsReturned Error
            end_times = get_list_or_404(Chart, time=end_time)
            json =Chart.getallstudents("range", start_time, end_time)# pass the datetime not the chart object in as start and end time
        else:
            raise Http404('No data type')
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
            stud = form.cleaned_data.get('str_student')
            Syncing.syncFitbitData(form.cleaned_data.get('sync_date'), stud)
            return redirect('syncsuccess', name = stud) 
    else:
        form = SyncUpload()
    return render(request, 'syncpage.html', {'form': form})
class SyncSuccess(View):
    
    def get(self, request, *args, **kwargs):
        name = self.kwargs['name']
        studentobj, dne = Student.returnObject(name)
        if 'DNE' in dne:
            raise Http404("Student does not exist") 
        synctime = Syncing.objects.filter(student_name=studentobj).latest('recent_synctime')
        synctime = synctime.recent_synctime
        return render(request, 'syncsuccess.html', {'synctime': synctime, 'name': name})

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

