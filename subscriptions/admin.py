from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'is_active']
    list_filter = ['plan_type', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status_colored', 'is_active_display', 'start_date', 'end_date', 'auto_renew']
    list_filter = ['status', 'plan', 'auto_renew']
    search_fields = ['user__username', 'user__email']
    date_hierarchy = 'start_date'
    ordering = ['-created_at']
    
    readonly_fields = ['is_active_display']
    
    actions = ['sync_with_user', 'activate_subscription', 'cancel_subscription']
    
    def status_colored(self, obj):
        colors = {
            'active': 'green',
            'cancelled': 'red',
            'expired': 'gray',
            'trial': 'orange'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    
    def is_active_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Ativa</span>')
        return format_html('<span style="color: red;">✗ Inativa</span>')
    is_active_display.short_description = 'Status Atual'
    
    def sync_with_user(self, request, queryset):
        """Sincroniza as assinaturas selecionadas com os campos do User"""
        from accounts.models import User
        synced = 0
        
        for subscription in queryset:
            user = subscription.user
            if subscription.is_active and subscription.plan.plan_type == 'pro':
                User.objects.filter(pk=user.pk).update(
                    is_premium=True,
                    subscription_start=subscription.start_date,
                    subscription_end=subscription.end_date
                )
            elif subscription.status in ['cancelled', 'expired']:
                User.objects.filter(pk=user.pk).update(
                    is_premium=False,
                    subscription_end=timezone.now().date()
                )
            synced += 1
        
        self.message_user(request, f'{synced} assinatura(s) sincronizada(s) com sucesso!')
    sync_with_user.short_description = 'Sincronizar com usuário'
    
    def activate_subscription(self, request, queryset):
        """Ativa as assinaturas selecionadas"""
        from accounts.models import User
        updated = queryset.update(status='active')
        
        # Sincroniza com o user
        for subscription in queryset:
            user = subscription.user
            if subscription.plan.plan_type == 'pro':
                User.objects.filter(pk=user.pk).update(
                    is_premium=True,
                    subscription_start=subscription.start_date,
                    subscription_end=subscription.end_date
                )
        self.message_user(request, f'{updated} assinatura(s) ativada(s)!')
    activate_subscription.short_description = 'Ativar assinaturas'
    
    def cancel_subscription(self, request, queryset):
        """Cancela as assinaturas selecionadas"""
        from accounts.models import User
        updated = queryset.update(status='cancelled')
        
        # Remove premium do user
        for subscription in queryset:
            user = subscription.user
            User.objects.filter(pk=user.pk).update(
                is_premium=False,
                subscription_end=timezone.now().date()
            )
        self.message_user(request, f'{updated} assinatura(s) cancelada(s)!')
    cancel_subscription.short_description = 'Cancelar assinaturas'

