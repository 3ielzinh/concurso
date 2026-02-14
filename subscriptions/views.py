from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Plan, Subscription


class PlansListView(ListView):
    """List all available plans"""
    model = Plan
    template_name = 'subscriptions/plans_list.html'
    context_object_name = 'plans'
    
    def get_queryset(self):
        return Plan.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_subscription'] = Subscription.objects.filter(
                user=self.request.user,
                status='active'
            ).first()
        return context


class MySubscriptionView(LoginRequiredMixin, TemplateView):
    """View user's current subscription"""
    template_name = 'subscriptions/my_subscription.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription'] = Subscription.objects.filter(
            user=self.request.user,
            status='active'
        ).first()
        context['all_plans'] = Plan.objects.filter(is_active=True)
        return context


class UpgradeView(LoginRequiredMixin, TemplateView):
    """
    Placeholder for upgrade functionality
    In production, this would integrate with payment gateway
    """
    template_name = 'subscriptions/upgrade.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan_type = self.kwargs.get('plan_type')
        context['plan'] = Plan.objects.filter(plan_type=plan_type, is_active=True).first()
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Handle upgrade (placeholder - integrate payment gateway here)
        """
        messages.info(
            request,
            'Funcionalidade de pagamento em desenvolvimento. '
            'Em breve você poderá fazer upgrade!'
        )
        return redirect('subscriptions:plans')
