from django.shortcuts import render
from .models import Recent, Day, Notes
# Create your views here.
def recent(request):
    recent = Recent.objects.all()
    return render(request, 'recent.html', {'recent': recent})

def day(request):
    day = Day.objects.all()
    return render(request, 'day.html', {'day': day})
