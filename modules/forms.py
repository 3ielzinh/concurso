from django import forms
from .models import StudySession, StudySchedule, Subject


def get_user_allowed_subjects(user):
    """
    Get all subjects that a user has access to based on allowed categories
    """
    # Import here to avoid circular import
    from user_management.models import UserModuleAccess
    
    # Check if user has custom module access configured
    try:
        module_access = UserModuleAccess.objects.get(user=user)
        allowed_categories = module_access.allowed_categories.all()
        if allowed_categories.exists():
            # User has specific categories assigned
            return Subject.objects.filter(
                module__category__in=allowed_categories,
                module__category__is_active=True,
                is_active=True
            )
    except UserModuleAccess.DoesNotExist:
        pass
    
    # Default to plan-based access
    if user.is_premium:
        return Subject.objects.filter(is_active=True)
    else:
        # Free users only see non-premium categories
        return Subject.objects.filter(
            module__category__is_premium=False,
            is_active=True
        )


class StudySessionForm(forms.ModelForm):
    """Form for creating/editing study sessions"""
    
    class Meta:
        model = StudySession
        fields = ['subject', 'date', 'hours', 'notes', 'completed']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hours': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter subjects based on user's allowed categories
            self.fields['subject'].queryset = get_user_allowed_subjects(user)


class StudyScheduleForm(forms.ModelForm):
    """Form for creating/editing study schedules"""
    
    class Meta:
        model = StudySchedule
        fields = ['subject', 'weekday', 'start_time', 'end_time', 'is_active']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'weekday': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filter subjects based on user's allowed categories
            self.fields['subject'].queryset = get_user_allowed_subjects(user)
