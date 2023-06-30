from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart, name='chart'),
    path('predict/',views.predict, name='predict'),
    path('retrain/', views.retrain, name='retrain'),
    path('data/',views.send_data,name='send_data'),
]