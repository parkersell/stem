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
from django.urls import path
from datavis.views import DataView, SingleChartView, ChartData, MultiChartView, SyncSuccess
from datavis import views as dv
from analysis import views as av

urlpatterns = [
    path('', dv.home, name='home'),
    path('recent/', av.recent, name='recent'),
    path('admin/', admin.site.urls),
    path('day/', av.day, name ='day'),
    path('upload/', DataView.as_view(), name="data_upload"),
    path('singlechart/', SingleChartView.as_view(), name='singlechart'),
    path('multichart/', MultiChartView.as_view(), name='multichart'),
    path('api/chart/data/', ChartData.as_view(), name='api-data'),
    path('sync/', dv.syncpage, name ='syncpage'),
    path('sync/success/<str:name>/', SyncSuccess.as_view(), name ='syncsuccess'),
    path('404', dv.v404, name ='four')


]
