from django import forms
from .models import Chart, Student
import io, csv
from datetime import datetime


class DataUpload(forms.Form):
    data_file = forms.FileField(label='Enter a csv file')

    def process_hr_data(self):
        def convert_date(str):
            data = datetime.strptime(str, '%m/%d/%Y %I:%M:%S %p')
            return data

        f = io.TextIOWrapper(self.cleaned_data['data_file'].file)
        reader = csv.DictReader(f)

        for hr in reader:
            Chart.objects.create(student_name=Student.objects.get(student_name="Parker"),
                                 time=convert_date(hr["Time"]),
                                 min_hr=hr["Value"],
                                 min_steps=0
                                 )
