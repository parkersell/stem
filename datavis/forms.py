from django import forms
from .models import Chart, Student, Syncing
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
            Chart.objects.create(student_name=Student.objects.get(student_name="Caiden"),
                                 time=convert_date(hr["Time"]),
                                 min_hr=hr["Value"]
                                 )

class SyncUpload(forms.Form):
    str_student= forms.CharField(
        label='Student', 
        help_text='Which student would you like to sync data for?',
        widget=forms.TextInput(), 
        max_length=30
    )
    sync_date = forms.CharField(
        label='Sync date',
        help_text='Choices are today, yesterday, or %Y-%m-%d', 
        widget=forms.TextInput(),
        max_length=30
    )
    class Meta:
        model =Syncing
        fields =['student_name', 'recent_synctime','str_student', 'sync_date']

class SingleChartSelect(forms.Form):
    student_str= forms.CharField(
        label='Student', 
        # help_text='Which student would you like to see data for?',
        widget=forms.TextInput(), 
        max_length=30
    )
    start_time=forms.CharField(
        label='Start time',
        widget=forms.TextInput(),
        max_length=30
    )
    end_time=forms.CharField(
        label='End time',
        widget=forms.TextInput(),
        max_length=30
    )

class MultiChartSelect(forms.Form):
    student_one= forms.CharField( 
        label='Student', 
        # help_text='Which student would you like to see data for?',
        widget=forms.TextInput(),
        max_length=30
    )
    student_two= forms.CharField(
        label='Student', 
        # help_text='Which other student would you like to see data for?',
        widget=forms.TextInput(),
        max_length=30
    )
    start_time=forms.CharField(
        label='Start time',
        widget=forms.TextInput(),
        max_length=30
    )
    end_time=forms.CharField(
        label='End time',
        widget=forms.TextInput(),
        max_length=30
    )