from django.db import models
from django.conf import settings


class StudyGoal(models.Model):
    """
    Monthly or custom period study goals
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_goals',
        verbose_name='Usuário'
    )
    title = models.CharField('Título', max_length=200)
    target_hours = models.DecimalField('Meta de Horas', max_digits=6, decimal_places=2)
    start_date = models.DateField('Data Início')
    end_date = models.DateField('Data Fim')
    is_completed = models.BooleanField('Concluída', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Meta de Estudo'
        verbose_name_plural = 'Metas de Estudo'
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @property
    def progress_hours(self):
        """Calculate hours studied in this goal period"""
        from modules.models import StudySession
        total = StudySession.objects.filter(
            user=self.user,
            date__gte=self.start_date,
            date__lte=self.end_date
        ).aggregate(models.Sum('hours'))['hours__sum']
        return total or 0
    
    @property
    def progress_percentage(self):
        """Calculate percentage of goal completion"""
        if self.target_hours == 0:
            return 0
        return min((self.progress_hours / self.target_hours) * 100, 100)


class StudyStreak(models.Model):
    """
    Track consecutive days of study (consistency)
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_streak',
        verbose_name='Usuário'
    )
    current_streak = models.IntegerField('Sequência Atual', default=0)
    longest_streak = models.IntegerField('Maior Sequência', default=0)
    last_study_date = models.DateField('Última Data de Estudo', null=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Sequência de Estudos'
        verbose_name_plural = 'Sequências de Estudos'
    
    def __str__(self):
        return f"{self.user.username} - {self.current_streak} dias"
    
    def update_streak(self, study_date):
        """Update streak based on new study session date"""
        from django.utils import timezone
        from datetime import timedelta
        
        if not self.last_study_date:
            # First study session
            self.current_streak = 1
            self.longest_streak = 1
        elif study_date == self.last_study_date:
            # Same day, no change
            return
        elif study_date == self.last_study_date + timedelta(days=1):
            # Consecutive day
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            # Streak broken
            self.current_streak = 1
        
        self.last_study_date = study_date
        self.save()
