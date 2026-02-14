from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from modules.models import StudySession, Progress, Category
from .models import StudyGoal, StudyStreak


class MetricsReportView(LoginRequiredMixin, ListView):
    """Comprehensive metrics and reports view"""
    template_name = 'metrics/report.html'
    context_object_name = 'study_sessions'
    
    def get_queryset(self):
        # Get last 30 days of study sessions
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        return StudySession.objects.filter(
            user=self.request.user,
            date__gte=thirty_days_ago
        ).order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Total hours studied
        context['total_hours'] = StudySession.objects.filter(
            user=user
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        
        # Last 7 days hours
        seven_days_ago = timezone.now().date() - timedelta(days=7)
        context['weekly_hours'] = StudySession.objects.filter(
            user=user,
            date__gte=seven_days_ago
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        
        # Last 30 days hours
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        context['monthly_hours'] = StudySession.objects.filter(
            user=user,
            date__gte=thirty_days_ago
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        
        # Progress by category
        # Import here to avoid circular import
        from modules.views import get_user_allowed_categories
        
        progress_data = []
        categories = get_user_allowed_categories(user)
        
        for category in categories:
            subjects_progress = Progress.objects.filter(
                user=user,
                subject__module__category=category
            )
            
            total_progress = subjects_progress.aggregate(
                avg_percentage=Sum('percentage')
            )['avg_percentage'] or 0
            
            total_hours = subjects_progress.aggregate(
                total_hours=Sum('total_hours')
            )['total_hours'] or 0
            
            if subjects_progress.exists():
                progress_data.append({
                    'category': category,
                    'progress': total_progress / subjects_progress.count(),
                    'hours': total_hours,
                    'subjects_count': subjects_progress.count()
                })
        
        context['progress_by_category'] = progress_data
        
        # Study streak
        streak, created = StudyStreak.objects.get_or_create(user=user)
        context['study_streak'] = streak
        
        # Current goals
        context['current_goals'] = StudyGoal.objects.filter(
            user=user,
            end_date__gte=timezone.now().date()
        )
        
        # Daily study data for chart (last 7 days)
        daily_data = []
        for i in range(6, -1, -1):
            date = timezone.now().date() - timedelta(days=i)
            hours = StudySession.objects.filter(
                user=user,
                date=date
            ).aggregate(Sum('hours'))['hours__sum'] or 0
            
            daily_data.append({
                'date': date.strftime('%d/%m'),
                'hours': float(hours)
            })
        
        context['daily_study_data'] = daily_data
        
        return context
