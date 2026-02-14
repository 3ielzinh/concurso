from django.core.management.base import BaseCommand
from django.utils import timezone
from subscriptions.models import Subscription


class Command(BaseCommand):
    help = 'Sincroniza todas as assinaturas existentes com os campos do modelo User'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Sincronizando assinaturas...'))
        
        subscriptions = Subscription.objects.all()
        synced_count = 0
        
        for subscription in subscriptions:
            user = subscription.user
            
            if subscription.is_active and subscription.plan.plan_type == 'pro':
                user.is_premium = True
                user.subscription_start = subscription.start_date
                user.subscription_end = subscription.end_date
                synced_count += 1
            elif subscription.status in ['cancelled', 'expired']:
                user.is_premium = False
                user.subscription_end = timezone.now().date()
                synced_count += 1
            
            user.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Sincronizado: {user.username} - {subscription.plan.name} ({subscription.status})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ {synced_count} assinatura(s) sincronizada(s) com sucesso!'
            )
        )
