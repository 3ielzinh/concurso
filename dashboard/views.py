from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from modules.models import StudySession, Progress, Category
from metrics.models import StudyGoal, StudyStreak


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard view with overview of all study metrics
    """
    template_name = 'dashboard/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Total hours studied (all time)
        context['total_hours'] = StudySession.objects.filter(
            user=user
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        
        # This week's hours
        week_start = timezone.now().date() - timedelta(days=timezone.now().weekday())
        context['weekly_hours'] = StudySession.objects.filter(
            user=user,
            date__gte=week_start
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        
        # This month's hours
        month_start = timezone.now().date().replace(day=1)
        context['monthly_hours'] = StudySession.objects.filter(
            user=user,
            date__gte=month_start
        ).aggregate(Sum('hours'))['hours__sum'] or 0
        
        # Study streak
        streak, created = StudyStreak.objects.get_or_create(user=user)
        context['study_streak'] = streak
        
        # Recent study sessions
        context['recent_sessions'] = StudySession.objects.filter(
            user=user
        ).select_related('subject', 'subject__module', 'subject__module__category')[:5]
        
        # Progress summary
        progress_summary = Progress.objects.filter(
            user=user
        ).aggregate(
            avg_progress=Sum('percentage'),
            completed=Count('id', filter=Q(is_completed=True)),
            total=Count('id')
        )
        
        if progress_summary['total'] > 0:
            context['avg_progress'] = progress_summary['avg_progress'] / progress_summary['total']
        else:
            context['avg_progress'] = 0
        
        context['completed_subjects'] = progress_summary['completed']
        context['total_subjects'] = progress_summary['total']
        
        # Current month goal
        current_goals = StudyGoal.objects.filter(
            user=user,
            start_date__lte=timezone.now().date(),
            end_date__gte=timezone.now().date()
        ).first()
        
        context['current_goal'] = current_goals
        
        # Categories overview (for quick access)
        # Import here to avoid circular import
        from modules.views import get_user_allowed_categories
        
        categories = get_user_allowed_categories(user)
        context['available_categories'] = categories[:6]  # Show first 6
        
        # Subscription status
        context['is_premium'] = user.is_premium
        context['has_active_subscription'] = user.has_active_subscription
        
        return context
