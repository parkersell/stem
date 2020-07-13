from django.db import models
from datavis.models import Student
# Create your models here.

class Notes(models.Model):
    teacher_name = models.CharField(max_length=30)
    student_name = models.ForeignKey(Student, max_length=30, related_name= 'notes', on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    time_referred = models.DateTimeField()
    note = models.TextField(max_length=4000)

class Day(models.Model):
    student_name = models.ForeignKey(Student, max_length=30, related_name= 'day', on_delete=models.CASCADE)
    peak_hr = models.IntegerField()
    day_str_red = models.IntegerField()
    str_step_cor = models.IntegerField()


class Recent(models.Model):
    student_name = models.ForeignKey(Student, max_length=30, related_name= 'recent', on_delete=models.CASCADE)
    avg_hr = models.IntegerField()
    times_str_red = models.IntegerField()
    time_rec_str_red = models.DateTimeField()
    str_step_cor = models.IntegerField()