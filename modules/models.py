from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Main study categories (Carreiras Policiais, Militares, etc.)
    """
    CATEGORY_CHOICES = [
        ('policiais', 'Carreiras Policiais'),
        ('militares', 'Carreiras Militares'),
        ('fiscais', 'Carreiras Fiscais'),
        ('juridicas', 'Carreiras Jurídicas'),
        ('bancarias', 'Carreiras Bancárias'),
        ('educacao', 'Educação'),
        ('saude', 'Saúde'),
        ('administrativa', 'Administrativa'),
        ('ti', 'TI'),
        ('engenharia', 'Engenharia'),
        ('fiscalizacao', 'Fiscalização'),
        ('logistica', 'Logística'),
        ('legislativa', 'Legislativa'),
        ('enem_vestibular', 'ENEM/Vestibulares'),
    ]
    
    name = models.CharField('Nome', max_length=100, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField('Descrição', blank=True)
    icon = models.CharField('Ícone', max_length=50, default='book')
    color = models.CharField('Cor', max_length=20, default='primary')
    background_image = models.URLField('Imagem de Fundo', max_length=500, blank=True, help_text='URL da imagem de fundo do card')
    is_premium = models.BooleanField('Requer Premium', default=False)
    order = models.IntegerField('Ordem', default=0)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.get_name_display()


class Module(models.Model):
    """
    Study modules within a category
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Categoria'
    )
    name = models.CharField('Nome', max_length=200)
    description = models.TextField('Descrição', blank=True)
    background_image = models.URLField('Imagem de Fundo', max_length=500, blank=True, help_text='URL da imagem de fundo do card')
    order = models.IntegerField('Ordem', default=0)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return f"{self.category} - {self.name}"


class Subject(models.Model):
    """
    Subjects/topics within a module
    """
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name='Módulo'
    )
    name = models.CharField('Nome', max_length=200)
    description = models.TextField('Descrição', blank=True)
    estimated_hours = models.DecimalField(
        'Horas Estimadas',
        max_digits=5,
        decimal_places=2,
        default=0
    )
    order = models.IntegerField('Ordem', default=0)
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'
        ordering = ['module', 'order', 'name']
    
    def __str__(self):
        return self.name


class StudySession(models.Model):
    """
    Individual study sessions logged by users
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='study_sessions',
        verbose_name='Usuário'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='study_sessions',
        verbose_name='Disciplina'
    )
    date = models.DateField('Data')
    hours = models.DecimalField('Horas Estudadas', max_digits=4, decimal_places=2)
    notes = models.TextField('Anotações', blank=True)
    completed = models.BooleanField('Concluído', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Sessão de Estudo'
        verbose_name_plural = 'Sessões de Estudo'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.subject.name} - {self.date}"


class Progress(models.Model):
    """
    Track user progress in each subject
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name='Usuário'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='progress',
        verbose_name='Disciplina'
    )
    percentage = models.DecimalField(
        'Percentual',
        max_digits=5,
        decimal_places=2,
        default=0,
        help_text='Percentual de conclusão'
    )
    total_hours = models.DecimalField(
        'Total de Horas',
        max_digits=6,
        decimal_places=2,
        default=0
    )
    is_completed = models.BooleanField('Concluído', default=False)
    last_studied = models.DateField('Último Estudo', null=True, blank=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Progresso'
        verbose_name_plural = 'Progressos'
        unique_together = ['user', 'subject']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.subject.name} ({self.percentage}%)"


class StudySchedule(models.Model):
    """
    Weekly study schedule for users
    """
    WEEKDAY_CHOICES = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Usuário'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Disciplina'
    )
    weekday = models.IntegerField('Dia da Semana', choices=WEEKDAY_CHOICES)
    start_time = models.TimeField('Hora Início')
    end_time = models.TimeField('Hora Fim')
    is_active = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Cronograma'
        verbose_name_plural = 'Cronogramas'
        ordering = ['weekday', 'start_time']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_weekday_display()} - {self.subject.name}"
