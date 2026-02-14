from django.contrib import admin
from .models import StudyGoal, StudyStreak


@admin.register(StudyGoal)
class StudyGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'target_hours', 'start_date', 'end_date', 'is_completed']
    list_filter = ['is_completed', 'start_date', 'end_date']
    search_fields = ['user__username', 'title']
    date_hierarchy = 'start_date'
    ordering = ['-start_date']


@admin.register(StudyStreak)
class StudyStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'last_study_date']
    search_fields = ['user__username']
    ordering = ['-current_streak']
