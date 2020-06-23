from django.db import models
from django.contrib.auth.models import User


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
    min_steps = models.IntegerField()

    def __str__(self):
        return str(self.time)


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



