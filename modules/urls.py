from django.urls import path
from . import views

app_name = 'modules'

urlpatterns = [
    # Categories and Modules
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('category/<str:category>/', views.ModuleListView.as_view(), name='module_list'),
    path('subject/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    
    # Study Sessions
    path('session/add/', views.StudySessionCreateView.as_view(), name='session_add'),
    path('session/<int:pk>/edit/', views.StudySessionUpdateView.as_view(), name='session_edit'),
    path('session/<int:pk>/delete/', views.StudySessionDeleteView.as_view(), name='session_delete'),
    
    # Study Schedule
    path('schedule/', views.StudyScheduleListView.as_view(), name='schedule_list'),
    path('schedule/add/', views.StudyScheduleCreateView.as_view(), name='schedule_add'),
    path('schedule/<int:pk>/edit/', views.StudyScheduleUpdateView.as_view(), name='schedule_edit'),
    path('schedule/<int:pk>/delete/', views.StudyScheduleDeleteView.as_view(), name='schedule_delete'),
]
