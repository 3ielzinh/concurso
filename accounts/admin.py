from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'full_name_display', 'subscription_status_display',
        'subscription_end', 'is_staff', 'date_joined'
    ]
    list_filter = ['is_premium', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    date_hierarchy = 'date_joined'
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('📱 Informações de Contato', {
            'fields': ('phone',)
        }),
        ('👤 Perfil', {
            'fields': ('profile_picture', 'bio', 'study_goal_hours')
        }),
        ('💎 Assinatura Premium', {
            'fields': ('is_premium', 'subscription_start', 'subscription_end'),
            'description': 'Configure o acesso premium do usuário. Marque "É Premium" para liberar conteúdo exclusivo.'
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Extras', {
            'fields': ('email', 'first_name', 'last_name', 'is_premium')
        }),
    )
    
    actions = ['make_premium', 'remove_premium', 'extend_subscription']
    
    def full_name_display(self, obj):
        return obj.get_full_name() or '-'
    full_name_display.short_description = 'Nome Completo'
    
    def subscription_status_display(self, obj):
        if obj.is_premium:
            if obj.subscription_end:
                days_left = (obj.subscription_end - timezone.now().date()).days
                if days_left < 0:
                    return format_html('<span style="color: red; font-weight: bold;">⚠️ Expirada</span>')
                elif days_left < 7:
                    return format_html('<span style="color: orange; font-weight: bold;">⚠️ Expira em {} dias</span>', days_left)
                else:
                    return format_html('<span style="color: green; font-weight: bold;">✓ Premium Ativo</span>')
            else:
                return format_html('<span style="color: green; font-weight: bold;">✓ Premium Vitalício</span>')
        return format_html('<span style="color: gray;">Gratuito</span>')
    subscription_status_display.short_description = 'Status da Assinatura'
    
    def make_premium(self, request, queryset):
        """Ativa assinatura premium para os usuários selecionados"""
        from datetime import timedelta
        today = timezone.now().date()
        end_date = today + timedelta(days=365)  # 1 ano
        
        updated = 0
        for user in queryset:
            user.is_premium = True
            user.subscription_start = today
            user.subscription_end = end_date
            user.save()
            updated += 1
        
        self.message_user(request, f'{updated} usuário(s) tornou-se Premium (1 ano)!')
    make_premium.short_description = '💎 Ativar Premium (1 ano)'
    
    def remove_premium(self, request, queryset):
        """Remove assinatura premium dos usuários selecionados"""
        updated = queryset.update(
            is_premium=False,
            subscription_end=timezone.now().date()
        )
        self.message_user(request, f'{updated} usuário(s) removido do Premium!')
    remove_premium.short_description = '❌ Remover Premium'
    
    def extend_subscription(self, request, queryset):
        """Estende a assinatura por mais 30 dias"""
        from datetime import timedelta
        updated = 0
        
        for user in queryset.filter(is_premium=True):
            if user.subscription_end:
                user.subscription_end = user.subscription_end + timedelta(days=30)
            else:
                user.subscription_end = timezone.now().date() + timedelta(days=30)
            user.save()
            updated += 1
        
        self.message_user(request, f'{updated} assinatura(s) estendida(s) por 30 dias!')
    extend_subscription.short_description = '📅 Estender Assinatura (30 dias)'
