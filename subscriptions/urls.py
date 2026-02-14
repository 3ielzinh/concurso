from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('plans/', views.PlansListView.as_view(), name='plans'),
    path('my-subscription/', views.MySubscriptionView.as_view(), name='my_subscription'),
    path('upgrade/<str:plan_type>/', views.UpgradeView.as_view(), name='upgrade'),
]
