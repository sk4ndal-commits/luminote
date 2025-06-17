from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from typing import Any, Dict
from django.db.models import Max
from django.utils import timezone
from datetime import timedelta

from .forms import CustomUserCreationForm, CustomAuthenticationForm
from subjects.models import Subject, Topic, Document

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
    Displays a dashboard with user's study information.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user

        # Get active subject (most recently updated)
        active_subject = Subject.objects.filter(user=user).order_by('-updated_at').first()
        context['active_subject'] = active_subject

        # Get active topic if there's an active subject
        active_topic = None
        if active_subject:
            active_topic = Topic.objects.filter(subject=active_subject).order_by('-updated_at').first()
        context['active_topic'] = active_topic

        # Get last action (most recent document upload)
        last_document = Document.objects.filter(subject__user=user).order_by('-uploaded_at').first()
        context['last_document'] = last_document

        # Calculate days since last activity
        days_since_last_activity = None
        if last_document and last_document.uploaded_at:
            time_diff = timezone.now() - last_document.uploaded_at
            days_since_last_activity = time_diff.days
        context['days_since_last_activity'] = days_since_last_activity

        # Progress overview
        # For simplicity, we'll calculate a basic progress metric:
        # - Count of documents per subject
        if active_subject:
            total_topics = Topic.objects.filter(subject=active_subject).count()
            topics_with_documents = Topic.objects.filter(
                subject=active_subject, 
                documents__isnull=False
            ).distinct().count()

            if total_topics > 0:
                progress_percentage = int((topics_with_documents / total_topics) * 100)
            else:
                progress_percentage = 0

            context['progress_percentage'] = progress_percentage

            # Find topics without documents (weak topics)
            weak_topics = Topic.objects.filter(
                subject=active_subject, 
                documents__isnull=True
            ).distinct()
            context['weak_topics'] = weak_topics

        return context
