from django.db import models
from django.conf import settings


class Plan(models.Model):
    """
    Subscription plans (Free, Pro, etc.)
    """
    PLAN_TYPES = [
        ('free', 'Gratuito'),
        ('police', 'Carreira Policial'),
        ('bank', 'Carreira Bancária'),
        ('enem', 'ENEM/Vestibular'),
        ('military', 'Carreira Militar'),
        ('legal', 'Carreira Jurídica'),
        ('fiscal', 'Carreira Fiscal'),
        ('pro', 'Pro - Acesso Total'),
    ]
    
    name = models.CharField('Nome', max_length=100)
    plan_type = models.CharField('Tipo', max_length=20, choices=PLAN_TYPES, unique=True)
    description = models.TextField('Descrição')
    price = models.DecimalField('Preço Mensal', max_digits=8, decimal_places=2)
    features = models.TextField('Recursos', help_text='Um recurso por linha')
    
    # Module access
    modules = models.ManyToManyField(
        'modules.Module',
        related_name='plans',
        verbose_name='Módulos Inclusos',
        blank=True,
        help_text='Módulos que este plano permite acessar'
    )
    
    # Access control
    max_categories = models.IntegerField('Máximo de Categorias', default=3)
    max_modules = models.IntegerField('Máximo de Módulos', default=10)
    has_premium_categories = models.BooleanField('Acesso a Categorias Premium', default=False)
    has_analytics = models.BooleanField('Relatórios Avançados', default=False)
    has_export = models.BooleanField('Exportar Dados', default=False)
    
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['price']
    
    def __str__(self):
        return self.name
    
    def get_features_list(self):
        """Return features as a list"""
        return [f.strip() for f in self.features.split('\n') if f.strip()]


class Subscription(models.Model):
    """
    User subscriptions
    """
    STATUS_CHOICES = [
        ('active', 'Ativa'),
        ('cancelled', 'Cancelada'),
        ('expired', 'Expirada'),
        ('trial', 'Período de Teste'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Usuário'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='Plano'
    )
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField('Data Início')
    end_date = models.DateField('Data Fim', null=True, blank=True)
    
    # Payment info (for future integration)
    payment_method = models.CharField('Método de Pagamento', max_length=50, blank=True)
    last_payment_date = models.DateField('Última Data de Pagamento', null=True, blank=True)
    next_payment_date = models.DateField('Próxima Data de Pagamento', null=True, blank=True)
    
    auto_renew = models.BooleanField('Renovação Automática', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self):
        """Check if subscription is currently active"""
        from django.utils import timezone
        if self.status != 'active':
            return False
        if self.end_date and self.end_date < timezone.now().date():
            return False
        return True
