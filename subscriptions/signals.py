from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Subscription


@receiver(post_save, sender=Subscription)
def sync_user_subscription(sender, instance, created, **kwargs):
    """
    Sincroniza os campos de assinatura do User quando uma Subscription é criada/atualizada
    """
    # Evita loop infinito
    if kwargs.get('raw', False):
        return
    
    user = instance.user
    
    # Verifica se a assinatura está ativa
    if instance.is_active and instance.plan.plan_type == 'pro':
        user.is_premium = True
        user.subscription_start = instance.start_date
        user.subscription_end = instance.end_date
    elif instance.status in ['cancelled', 'expired']:
        # Se a assinatura foi cancelada ou expirou, remove o premium
        user.is_premium = False
        user.subscription_end = timezone.now().date()
    
    # Salva sem disparar signals do User
    User = user.__class__
    User.objects.filter(pk=user.pk).update(
        is_premium=user.is_premium,
        subscription_start=user.subscription_start,
        subscription_end=user.subscription_end
    )


@receiver(post_delete, sender=Subscription)
def remove_user_subscription(sender, instance, **kwargs):
    """
    Remove o premium do usuário quando a assinatura é deletada
    """
    user = instance.user
    
    # Salva sem disparar signals do User
    User = user.__class__
    User.objects.filter(pk=user.pk).update(
        is_premium=False,
        subscription_end=timezone.now().date()
    )
