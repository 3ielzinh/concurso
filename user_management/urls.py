from django.urls import path
from . import views

app_name = 'user_management'

urlpatterns = [
    # User list and search
    path('', views.user_list, name='user_list'),
    
    # User details and management
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('<int:user_id>/toggle-status/', views.user_toggle_status, name='user_toggle_status'),
    
    # Module access management
    path('<int:user_id>/module-access/', views.user_module_access, name='user_module_access'),
    
    # Password management
    path('<int:user_id>/reset-password/', views.user_reset_password, name='user_reset_password'),
    
    # Admin notes
    path('<int:user_id>/add-note/', views.user_add_note, name='user_add_note'),
    path('notes/<int:note_id>/delete/', views.user_delete_note, name='user_delete_note'),
]
