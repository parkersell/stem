from django.db import models
from django.contrib.auth.models import User

import fitbit
from fitbit import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
import json

class DataFile(models.Model):
    file = models.FileField(upload_to="student/%Y/%m/%d")


class Student(models.Model):
    student_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.student_name


class Chart(models.Model):
    student_name = models.ForeignKey(Student, max_length=30, related_name= 'chart', on_delete=models.CASCADE)
    time = models.DateTimeField(unique=True)
    min_hr = models.IntegerField()
    min_steps = models.IntegerField(null =True)

    def __str__(self):
        return str(self.time)

    def syncFitbitData(day, student):# could make into a class and use several different urls or could make one that updated every students for the day
        def convert_date(str, day):
                
                
                str = day+" "+str
                data = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M:%S')
                return data

        CLIENT_ID = '22BN3W'
        CLIENT_SECRET = 'c06b1ffc7da46f07517230dd15dc2fe4'

        server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
        server.browser_authorize()
        ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
        REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
        auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
        if (day == "yesterday"):
            yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
            day = yesterday 
        if (day == "today"):
            today = str(datetime.datetime.now().strftime("%Y-%m-%d"))
            day = today

        fit_statsHR = auth2_client.intraday_time_series('activities/heart', base_date=day, detail_level='1min') #form is base_date='2020-06-03'
        fit_statsStep = auth2_client.intraday_time_series('activities/steps', base_date=day, detail_level='1min')
        time_list = []
        time2_list = [] #not used 
        hr_list = []
        step_list =[]
        for i in fit_statsHR['activities-heart-intraday']['dataset']:
            hr_list.append(i['value'])
            time_list.append(i['time'])

        for i in fit_statsStep['activities-steps-intraday']['dataset']:
            step_list.append(i['value'])
            time2_list.append(i['time'])

        for i in range(len(time_list)):
            Chart.objects.create(student_name=Student.objects.get(student_name=student),
                                        time=convert_date(time_list[i], today),
                                        min_hr=hr_list[i]
                                        )

    def getonestudent(student, periodoftime): # returns a dictionary of last hour heart rate for specified student and period of time - hour, all
        studentobject = Student.objects.get(student_name=student)
        timetemp = Chart.objects.filter(student_name=studentobject).values_list('time', flat=True).order_by('-time')
        min_hrtemp = Chart.objects.filter(student_name=studentobject).values_list('min_hr', flat=True).order_by('-time')
        if (str(periodoftime)== "hour"):
            timetemp = timetemp[:60]
            min_hrtemp = min_hrtemp[:60] 
        time = []
        min_hr =[]
        for date in timetemp:
            time.append(str(date))
        for hr in min_hrtemp:
            min_hr.append(hr)
        time.reverse()
        min_hr.reverse()
        zipObj = zip(time, min_hr)
        return dict(zipObj)


    def getallstudents():
        data ={} #held to hold the dictionary on line 41
        labels =[]

        students = Student.objects.all() # should adjust to all with data
        numberofstudents = len(students)
        for student in students:
            labels.append(student.student_name)
            d = Chart.getonestudent(student.student_name, "hour")
            data.update({student.student_name: d}) # line 41 
        
        temp = {}
        temp.update({'labels': labels})
        for i in range(numberofstudents):
            name = str(labels[i])
            specificstudentdata = data[str(labels[i])]
            temp.update({name: specificstudentdata})
        return temp
        

        



class Notes(models.Model):
    teacher_name = models.CharField(max_length=30)
    student_name = models.ForeignKey(Student, max_length=30, related_name= 'notes', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    time_referred = models.DateTimeField()
    note = models.TextField(max_length=4000)


class Rec(models.Model):
    student_name = models.ForeignKey(Student, max_length=30, related_name= 'recent', on_delete=models.CASCADE)
    avg_hr = models.IntegerField()
    rec_sync = models.DateTimeField()
    times_str_red = models.IntegerField()
    time_rec_str_red = models.DateTimeField()
    str_step_cor = models.IntegerField()


class Day(models.Model):
    student_name = models.ForeignKey(Student, max_length=30, related_name= 'day', on_delete=models.CASCADE)
    peak_hr = models.IntegerField()
    day_str_red = models.IntegerField()
    str_step_cor = models.IntegerField()



