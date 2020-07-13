from django.urls import resolve, reverse
from django.test import TestCase
from .views import home, ChartView
from .models import Student, Chart
import datetime

class HomeTests(TestCase):
    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

class ChartTests(TestCase):
    def setUp(self):
        so= Student.objects.create(student_name='Django')
        Chart.objects.create(student_name=so, time=datetime.datetime.now(), min_hr=70)

    def test_chart_view_success_status_code(self):
        url = reverse('hrchart', kwargs={'name': "Django"})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_chart_view_not_found_status_code(self):
        url = reverse('hrchart', kwargs={'name': "Nobody"})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_chart_url_resolves_chart_view(self):
        view = resolve('/chart/Django/')
        self.assertEquals(view.func.__name__, ChartView.as_view().__name__)
    
    def django_test_example(self):
        request = RequestFactory().get('/chart/Django')
        view = ChartView()
        view.setup(request)

        context = view.get()
        self.assertIn('name', context)