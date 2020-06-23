from django.shortcuts import render

import csv, io
from django.contrib import messages
# Create your views here.
from .models import Rec, Day, Chart, Student
from django.views.generic.edit import FormView, View
from datetime import datetime
from .forms import DataUpload
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response

print("http://localhost:8000/chart")
def recent(request):
    recent = Rec.objects.all()
    return render(request, 'recent.html', {'recent': recent})

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'charts_ex.html', {"customers": 10})

def get_data(request, *args, **kwargs): # simple json response without rest api
    data = {
        "sales": 100, 
        "customers": 10,
    }
    return JsonResponse(data=data)

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        data ={} #held to hold the dictionary on line 41
        labels =[]

        students = Student.objects.all() # should adjust to all with data
        tot = len(students)
        for student in students:
            labels.append(student.student_name)
            timetemp = Chart.objects.filter(student_name=student).values_list('time', flat=True)
            min_hr = Chart.objects.filter(student_name=student).values_list('min_hr', flat=True)
            time = []
            for date in timetemp:
                time.append(str(date))
            zipObj = zip(time, min_hr)
            d = dict(zipObj)
            data.update({student.student_name: d}) # line 41 
        
        json = {
            'labels': labels, 
            str(labels[0]): data[str(labels[0])],
            str(labels[1]): data[str(labels[1])], 
        } 
        return Response(json)

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

"""
def datahr(request):
    data ={} #held to hold the dictionary on line 41
    labels =[]

    students = Student.objects.all() # should adjust to all with data
    tot = len(students)
    for student in students:
        labels.append(student.student_name)
        timetemp = Chart.objects.filter(student_name=student).values_list('time', flat=True)
        min_hr = Chart.objects.filter(student_name=student).values_list('min_hr', flat=True)
        time = []
        for date in timetemp:
            time.append(str(date))
        zipObj = zip(time, min_hr)
        d = dict(zipObj)
        data.update({student.student_name: d}) # line 41 
    
    json = {
        'labels': labels, 
        str(labels[0]): data[str(labels[0])],
        str(labels[1]): data[str(labels[1])], 
    }
    return JsonResponse(data=json)
"""
    
        


