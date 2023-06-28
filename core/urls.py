from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart, name='chart'),
    path('predict/',views.predict, name='predict')
]