"""stem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from datavis.views import DataView, HomeView, ChartData
from datavis import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^recent/$', views.recent, name='recent'),
    url('admin/', admin.site.urls),
    url(r'^day/$', views.day, name ='day'),
    url(r'upload/$', DataView.as_view(), name="data_upload"),
    url(r'^chart', HomeView.as_view(), name='hrchart'),
    # url(r'^api/data/$', get_data, name='api-data'),
    url(r'^api/chart/data/$', ChartData.as_view(), name='api-data'),
    #path('datahr', views.datahr, name='datahrchart'),
    url(r'^sync/$', views.syncdata, name ='syncdata')


]
