from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any, Dict

from .forms import CustomUserCreationForm, CustomAuthenticationForm

class RegisterView(CreateView):
    """
    View for user registration.
    """
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        If the form is valid, save the user and log them in.
        """
        response = super().form_valid(form)
        # Log the user in after registration
        login(self.request, self.object)
        return response

class CustomLoginView(LoginView):
    """
    View for user login.
    """
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    """
    View for user logout.
    """
    # Use the LOGOUT_REDIRECT_URL setting from settings.py
    # This ensures consistency with Django's built-in logout handling
    next_page = reverse_lazy('login')

class HomeView(LoginRequiredMixin, TemplateView):
    """
    Home view that requires login.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
