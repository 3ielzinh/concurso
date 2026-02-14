from django.contrib import admin
from .models import Category, Module, Subject, StudySession, Progress, StudySchedule


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_premium', 'order', 'is_active']
    list_filter = ['is_premium', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'description', 'order', 'is_active')
        }),
        ('Aparência', {
            'fields': ('icon', 'color', 'background_image'),
            'description': 'URL da imagem de fundo do card (ex: https://exemplo.com/imagem.jpg)'
        }),
        ('Permissões', {
            'fields': ('is_premium',)
        }),
    )


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['category', 'order']
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('category', 'name', 'description', 'order', 'is_active')
        }),
        ('Aparência', {
            'fields': ('background_image',),
            'description': 'URL da imagem de fundo do card (ex: https://exemplo.com/imagem.jpg)'
        }),
    )


class SubjectInline(admin.TabularInline):
    model = Subject
    extra = 1


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'module', 'estimated_hours', 'order', 'is_active']
    list_filter = ['module__category', 'module', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['module', 'order']


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'date', 'hours', 'completed']
    list_filter = ['completed', 'date', 'subject__module__category']
    search_fields = ['user__username', 'subject__name', 'notes']
    date_hierarchy = 'date'
    ordering = ['-date']


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'percentage', 'total_hours', 'is_completed', 'last_studied']
    list_filter = ['is_completed', 'subject__module__category']
    search_fields = ['user__username', 'subject__name']
    ordering = ['-last_studied']


@admin.register(StudySchedule)
class StudyScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'weekday', 'start_time', 'end_time', 'is_active']
    list_filter = ['weekday', 'is_active']
    search_fields = ['user__username', 'subject__name']
    ordering = ['weekday', 'start_time']
