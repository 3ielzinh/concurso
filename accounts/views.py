from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login, logout
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from .models import User
from .forms import CustomUserCreationForm, UserProfileForm


class UserRegisterView(CreateView):
    """View for user registration"""
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Conta criada com sucesso! Bem-vindo!')
        return response


class UserLoginView(LoginView):
    """View for user login"""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, f'Bem-vindo de volta, {form.get_user().first_name}!')
        return super().form_valid(form)


class UserLogoutView(View):
    """View for user logout"""
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Você saiu da sua conta.')
            logout(request)
        return redirect('accounts:login')
    
    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    """View for user profile management"""
    model = User
    form_class = UserProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)
