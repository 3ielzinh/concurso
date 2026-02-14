from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum, Q
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Category, Module, Subject, StudySession, StudySchedule, Progress
from .forms import StudySessionForm, StudyScheduleForm


def get_user_allowed_categories(user):
    """
    Get all categories that a user has access to.
    Priority:
    1. If user has specific allowed_categories in UserModuleAccess, use those
    2. Otherwise, use plan-based access (is_premium)
    """
    # Check if user has custom module access configured
    if hasattr(user, 'module_access'):
        allowed_categories = user.module_access.allowed_categories.all()
        if allowed_categories.exists():
            # User has specific categories assigned
            return allowed_categories.filter(is_active=True)
    
    # Default to plan-based access
    queryset = Category.objects.filter(is_active=True)
    if not user.is_premium:
        queryset = queryset.filter(is_premium=False)
    
    return queryset


class CategoryListView(LoginRequiredMixin, ListView):
    """List all available categories for the user"""
    model = Category
    template_name = 'modules/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return get_user_allowed_categories(self.request.user)


class ModuleListView(LoginRequiredMixin, ListView):
    """List modules within a category"""
    model = Module
    template_name = 'modules/module_list.html'
    context_object_name = 'modules'
    
    def get_queryset(self):
        category_name = self.kwargs.get('category')
        category = get_object_or_404(Category, name=category_name, is_active=True)
        
        # Check if user has access to this category
        allowed_categories = get_user_allowed_categories(self.request.user)
        if category not in allowed_categories:
            raise Http404("Você não tem permissão para acessar esta categoria.")
        
        return Module.objects.filter(
            category__name=category_name,
            is_active=True
        ).prefetch_related('subjects')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_name = self.kwargs.get('category')
        context['category'] = Category.objects.get(name=category_name)
        return context


class SubjectDetailView(LoginRequiredMixin, DetailView):
    """Detail view for a subject with progress"""
    model = Subject
    template_name = 'modules/subject_detail.html'
    context_object_name = 'subject'
    
    def get_object(self, queryset=None):
        subject = super().get_object(queryset)
        
        # Check if user has access to this subject's category
        allowed_categories = get_user_allowed_categories(self.request.user)
        if subject.module.category not in allowed_categories:
            raise Http404("Você não tem permissão para acessar este conteúdo.")
        
        return subject
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = self.get_object()
        
        # Get or create progress for this user/subject
        progress, created = Progress.objects.get_or_create(
            user=self.request.user,
            subject=subject
        )
        context['progress'] = progress
        
        # Get recent study sessions
        context['study_sessions'] = StudySession.objects.filter(
            user=self.request.user,
            subject=subject
        )[:10]
        
        return context


class StudySessionCreateView(LoginRequiredMixin, CreateView):
    """Create a new study session"""
    model = StudySession
    form_class = StudySessionForm
    template_name = 'modules/study_session_form.html'
    success_url = reverse_lazy('dashboard:home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        
        # Update progress
        subject = form.instance.subject
        progress, created = Progress.objects.get_or_create(
            user=self.request.user,
            subject=subject
        )
        
        # Calculate total hours
        total_hours = StudySession.objects.filter(
            user=self.request.user,
            subject=subject
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        
        progress.total_hours = total_hours
        progress.last_studied = form.instance.date
        
        # Calculate percentage (assuming estimated_hours is set)
        if subject.estimated_hours > 0:
            progress.percentage = min((total_hours / subject.estimated_hours) * 100, 100)
            if progress.percentage >= 100:
                progress.is_completed = True
        
        progress.save()
        
        messages.success(self.request, 'Sessão de estudo registrada com sucesso!')
        return response


class StudySessionUpdateView(LoginRequiredMixin, UpdateView):
    """Update a study session"""
    model = StudySession
    form_class = StudySessionForm
    template_name = 'modules/study_session_form.html'
    success_url = reverse_lazy('dashboard:home')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Sessão de estudo atualizada!')
        return super().form_valid(form)


class StudySessionDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a study session"""
    model = StudySession
    template_name = 'modules/study_session_confirm_delete.html'
    success_url = reverse_lazy('dashboard:home')
    
    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Sessão de estudo excluída!')
        return super().delete(request, *args, **kwargs)


class StudyScheduleListView(LoginRequiredMixin, ListView):
    """List user's study schedules"""
    model = StudySchedule
    template_name = 'modules/schedule_list.html'
    context_object_name = 'schedules'
    
    def get_queryset(self):
        return StudySchedule.objects.filter(user=self.request.user, is_active=True)


class StudyScheduleCreateView(LoginRequiredMixin, CreateView):
    """Create a new study schedule"""
    model = StudySchedule
    form_class = StudyScheduleForm
    template_name = 'modules/schedule_form.html'
    success_url = reverse_lazy('modules:schedule_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Cronograma criado com sucesso!')
        return super().form_valid(form)


class StudyScheduleUpdateView(LoginRequiredMixin, UpdateView):
    """Update a study schedule"""
    model = StudySchedule
    form_class = StudyScheduleForm
    template_name = 'modules/schedule_form.html'
    success_url = reverse_lazy('modules:schedule_list')
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_queryset(self):
        return StudySchedule.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Cronograma atualizado!')
        return super().form_valid(form)


class StudyScheduleDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a study schedule"""
    model = StudySchedule
    template_name = 'modules/schedule_confirm_delete.html'
    success_url = reverse_lazy('modules:schedule_list')
    
    def get_queryset(self):
        return StudySchedule.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cronograma excluído!')
        return super().delete(request, *args, **kwargs)
