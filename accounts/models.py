from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with additional fields for the SaaS platform
    """
    email = models.EmailField('Email', unique=True)
    phone = models.CharField('Telefone', max_length=20, blank=True)
    profile_picture = models.ImageField(
        'Foto de Perfil',
        upload_to='profiles/',
        blank=True,
        null=True
    )
    bio = models.TextField('Biografia', blank=True)
    
    # Study preferences
    study_goal_hours = models.DecimalField(
        'Meta de Horas Mensais',
        max_digits=5,
        decimal_places=2,
        default=40.00
    )
    
    # Subscription
    is_premium = models.BooleanField('É Premium', default=False)
    subscription_start = models.DateField('Início da Assinatura', null=True, blank=True)
    subscription_end = models.DateField('Fim da Assinatura', null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    @property
    def has_active_subscription(self):
        """Check if user has an active premium subscription"""
        if not self.is_premium:
            return False
        # Se não tem data de expiração, é assinatura vitalícia/permanente
        if not self.subscription_end:
            return True
        # Verifica se a assinatura não expirou
        from django.utils import timezone
        return self.subscription_end >= timezone.now().date()
