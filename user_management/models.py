from django.db import models
from django.conf import settings
from modules.models import Category


class UserModuleAccess(models.Model):
    """
    Controls which modules/categories each user has access to
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='module_access',
        verbose_name='Usuário'
    )
    allowed_categories = models.ManyToManyField(
        Category,
        related_name='allowed_users',
        verbose_name='Categorias Permitidas',
        blank=True
    )
    custom_access_level = models.CharField(
        'Nível de Acesso Customizado',
        max_length=50,
        blank=True,
        help_text='Nível de acesso especial além do plano'
    )
    notes = models.TextField('Observações', blank=True)
    
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Acesso a Módulos'
        verbose_name_plural = 'Acessos a Módulos'
    
    def __str__(self):
        return f"Acesso de {self.user.username}"


class UserAccessLog(models.Model):
    """
    Log of user access and activity for admin monitoring
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='access_logs',
        verbose_name='Usuário'
    )
    action = models.CharField('Ação', max_length=255)
    ip_address = models.GenericIPAddressField('Endereço IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    timestamp = models.DateTimeField('Data/Hora', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log de Acesso'
        verbose_name_plural = 'Logs de Acesso'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"


class UserAdminNote(models.Model):
    """
    Admin notes about users for internal tracking
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_notes',
        verbose_name='Usuário'
    )
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_notes',
        verbose_name='Administrador'
    )
    note = models.TextField('Nota')
    is_important = models.BooleanField('Importante', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Nota Administrativa'
        verbose_name_plural = 'Notas Administrativas'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Nota sobre {self.user.username} - {self.created_at.date()}"
