from django.urls import path
from . import views

app_name = 'metrics'

urlpatterns = [
    path('report/', views.MetricsReportView.as_view(), name='report'),
]
