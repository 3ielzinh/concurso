from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from datetime import datetime

from .models import UserModuleAccess, UserAccessLog, UserAdminNote
from .forms import (
    UserSearchForm, UserEditForm, UserModuleAccessForm,
    UserAdminNoteForm, UserPasswordResetForm
)
from modules.models import Category
from subscriptions.models import Subscription

User = get_user_model()


def is_admin(user):
    """Check if user is admin or staff"""
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@login_required
@user_passes_test(is_admin)
def user_list(request):
    """List all users with search and filters"""
    users = User.objects.annotate(
        active_subscriptions=Count('subscriptions', filter=Q(subscriptions__status='active'))
    ).select_related().order_by('-created_at')
    
    # Apply search and filters
    form = UserSearchForm(request.GET or None)
    if form.is_valid():
        search = form.cleaned_data.get('search')
        if search:
            users = users.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        
        is_active = form.cleaned_data.get('is_active')
        if is_active:
            users = users.filter(is_active=(is_active == 'true'))
        
        is_premium = form.cleaned_data.get('is_premium')
        if is_premium:
            users = users.filter(is_premium=(is_premium == 'true'))
        
        date_from = form.cleaned_data.get('date_from')
        if date_from:
            users = users.filter(created_at__date__gte=date_from)
        
        date_to = form.cleaned_data.get('date_to')
        if date_to:
            users = users.filter(created_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'premium_users': User.objects.filter(is_premium=True).count(),
        'new_this_month': User.objects.filter(
            created_at__month=timezone.now().month,
            created_at__year=timezone.now().year
        ).count(),
    }
    
    context = {
        'page_obj': page_obj,
        'form': form,
        'stats': stats,
    }
    return render(request, 'user_management/user_list.html', context)


@login_required
@user_passes_test(is_admin)
def user_detail(request, user_id):
    """View user details"""
    user = get_object_or_404(User, pk=user_id)
    
    # Get user's module access
    module_access, created = UserModuleAccess.objects.get_or_create(user=user)
    
    # Get user's subscriptions
    subscriptions = user.subscriptions.all().order_by('-created_at')[:5]
    
    # Get user's recent access logs
    access_logs = user.access_logs.all()[:20]
    
    # Get admin notes
    admin_notes = user.admin_notes.all()
    
    # Get study statistics
    from modules.models import StudySession
    study_sessions = StudySession.objects.filter(user=user)
    total_study_hours = sum([s.duration for s in study_sessions])
    
    context = {
        'user_obj': user,
        'module_access': module_access,
        'subscriptions': subscriptions,
        'access_logs': access_logs,
        'admin_notes': admin_notes,
        'total_study_hours': total_study_hours,
        'study_sessions_count': study_sessions.count(),
    }
    return render(request, 'user_management/user_detail.html', context)


@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    """Edit user information"""
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            
            # Log the action
            UserAccessLog.objects.create(
                user=user,
                action=f"Informações editadas por {request.user.username}"
            )
            
            messages.success(request, f'Usuário {user.username} atualizado com sucesso!')
            return redirect('user_management:user_detail', user_id=user.id)
    else:
        form = UserEditForm(instance=user)
    
    context = {
        'form': form,
        'user_obj': user,
    }
    return render(request, 'user_management/user_edit.html', context)


@login_required
@user_passes_test(is_admin)
def user_module_access(request, user_id):
    """Manage user's module access"""
    user = get_object_or_404(User, pk=user_id)
    module_access, created = UserModuleAccess.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserModuleAccessForm(request.POST, instance=module_access)
        if form.is_valid():
            form.save()
            
            # Log the action
            UserAccessLog.objects.create(
                user=user,
                action=f"Acesso a módulos modificado por {request.user.username}"
            )
            
            messages.success(request, f'Acesso aos módulos de {user.username} atualizado!')
            return redirect('user_management:user_detail', user_id=user.id)
    else:
        form = UserModuleAccessForm(instance=module_access)
    
    context = {
        'form': form,
        'user_obj': user,
        'all_categories': Category.objects.all(),
    }
    return render(request, 'user_management/user_module_access.html', context)


@login_required
@user_passes_test(is_admin)
def user_add_note(request, user_id):
    """Add admin note about user"""
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UserAdminNoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = user
            note.admin = request.user
            note.save()
            
            messages.success(request, 'Nota adicionada com sucesso!')
            return redirect('user_management:user_detail', user_id=user.id)
    else:
        form = UserAdminNoteForm()
    
    context = {
        'form': form,
        'user_obj': user,
    }
    return render(request, 'user_management/user_add_note.html', context)


@login_required
@user_passes_test(is_admin)
def user_delete_note(request, note_id):
    """Delete an admin note"""
    note = get_object_or_404(UserAdminNote, pk=note_id)
    user_id = note.user.id
    
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Nota excluída com sucesso!')
    
    return redirect('user_management:user_detail', user_id=user_id)


@login_required
@user_passes_test(is_admin)
def user_reset_password(request, user_id):
    """Admin resets user password"""
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        form = UserPasswordResetForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            
            # Log the action
            UserAccessLog.objects.create(
                user=user,
                action=f"Senha redefinida por {request.user.username}"
            )
            
            messages.success(request, f'Senha de {user.username} redefinida com sucesso!')
            return redirect('user_management:user_detail', user_id=user.id)
    else:
        form = UserPasswordResetForm()
    
    context = {
        'form': form,
        'user_obj': user,
    }
    return render(request, 'user_management/user_reset_password.html', context)


@login_required
@user_passes_test(is_admin)
def user_delete(request, user_id):
    """Delete user account"""
    user = get_object_or_404(User, pk=user_id)
    
    # Prevent deleting yourself
    if user == request.user:
        messages.error(request, 'Você não pode excluir sua própria conta!')
        return redirect('user_management:user_list')
    
    # Prevent deleting superusers
    if user.is_superuser and not request.user.is_superuser:
        messages.error(request, 'Você não tem permissão para excluir este usuário!')
        return redirect('user_management:user_list')
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'Usuário {username} excluído com sucesso!')
        return redirect('user_management:user_list')
    
    context = {
        'user_obj': user,
    }
    return render(request, 'user_management/user_delete.html', context)


@login_required
@user_passes_test(is_admin)
def user_toggle_status(request, user_id):
    """Toggle user active status"""
    user = get_object_or_404(User, pk=user_id)
    
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        
        status = 'ativado' if user.is_active else 'desativado'
        
        # Log the action
        UserAccessLog.objects.create(
            user=user,
            action=f"Conta {status} por {request.user.username}"
        )
        
        messages.success(request, f'Usuário {user.username} {status} com sucesso!')
    
    return redirect('user_management:user_detail', user_id=user.id)
