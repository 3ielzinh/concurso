from django import forms
from django.contrib.auth import get_user_model
from modules.models import Category
from subscriptions.models import Plan
from .models import UserModuleAccess, UserAdminNote

User = get_user_model()


class UserSearchForm(forms.Form):
    """Form for searching and filtering users"""
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nome, email ou username...'
        })
    )
    is_active = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos'), ('true', 'Ativos'), ('false', 'Inativos')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    is_premium = forms.ChoiceField(
        required=False,
        choices=[('', 'Todos'), ('true', 'Premium'), ('false', 'Gratuito')],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )


class UserEditForm(forms.ModelForm):
    """Form for editing user information"""
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'phone', 'is_active', 'is_staff', 'is_premium',
            'subscription_start', 'subscription_end', 'study_goal_hours'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_premium': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'subscription_start': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'subscription_end': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'study_goal_hours': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.5'
            }),
        }


class UserModuleAccessForm(forms.ModelForm):
    """Form for managing user's module access"""
    
    class Meta:
        model = UserModuleAccess
        fields = ['allowed_categories', 'custom_access_level', 'notes']
        widgets = {
            'allowed_categories': forms.CheckboxSelectMultiple(),
            'custom_access_level': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }


class UserAdminNoteForm(forms.ModelForm):
    """Form for adding admin notes about users"""
    
    class Meta:
        model = UserAdminNote
        fields = ['note', 'is_important']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Adicione uma nota sobre este usuário...'
            }),
            'is_important': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class UserPasswordResetForm(forms.Form):
    """Form for admin to reset user password"""
    new_password = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite a nova senha'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirme a nova senha'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')
        
        if password and confirm and password != confirm:
            raise forms.ValidationError('As senhas não coincidem.')
        
        return cleaned_data
