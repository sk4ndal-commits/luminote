from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from .models import Subject
from .forms import SubjectForm

class SubjectListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of subjects belonging to the current user.
    """
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        """
        Return only subjects belonging to the current user.
        """
        return Subject.objects.filter(user=self.request.user)

class SubjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    View for displaying details of a specific subject.
    """
    model = Subject
    template_name = 'subjects/subject_detail.html'
    context_object_name = 'subject'

    def test_func(self):
        """
        Ensure the subject belongs to the current user.
        """
        subject = self.get_object()
        return subject.user == self.request.user

class SubjectCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new subject.
    """
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    success_url = reverse_lazy('subject_list')

    def get_form_kwargs(self):
        """
        Pass the current user to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """
        Set the user and display a success message.
        """
        messages.success(self.request, _('Subject created successfully.'))
        return super().form_valid(form)

class SubjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating an existing subject.
    """
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'

    def test_func(self):
        """
        Ensure the subject belongs to the current user.
        """
        subject = self.get_object()
        return subject.user == self.request.user

    def get_success_url(self):
        """
        Return to the detail view of the updated subject.
        """
        return reverse_lazy('subject_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        """
        Display a success message.
        """
        messages.success(self.request, _('Subject updated successfully.'))
        return super().form_valid(form)

class SubjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a subject.
    """
    model = Subject
    template_name = 'subjects/subject_confirm_delete.html'
    success_url = reverse_lazy('subject_list')

    def test_func(self):
        """
        Ensure the subject belongs to the current user.
        """
        subject = self.get_object()
        return subject.user == self.request.user

    def delete(self, request, *args, **kwargs):
        """
        Display a success message.
        """
        messages.success(request, _('Subject deleted successfully.'))
        return super().delete(request, *args, **kwargs)
