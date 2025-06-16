from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect

from .models import Subject, Document
from .forms import SubjectForm, DocumentForm

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

    def get_context_data(self, **kwargs):
        """
        Add documents to context.
        """
        context = super().get_context_data(**kwargs)
        context['documents'] = self.object.documents.all().order_by('-uploaded_at')
        return context

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


class DocumentUploadView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View for uploading documents to a subject.
    """
    model = Document
    form_class = DocumentForm
    template_name = 'subjects/document_form.html'

    def setup(self, request, *args, **kwargs):
        """
        Set up the view with the subject.
        """
        super().setup(request, *args, **kwargs)
        self.subject = get_object_or_404(Subject, pk=kwargs.get('subject_pk'))

    def test_func(self):
        """
        Ensure the subject belongs to the current user.
        """
        return self.subject.user == self.request.user

    def get_form_kwargs(self):
        """
        Pass the subject to the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['subject'] = self.subject
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Add subject to context.
        """
        context = super().get_context_data(**kwargs)
        context['subject'] = self.subject
        return context

    def get_success_url(self):
        """
        Return to the subject detail page.
        """
        return reverse('subject_detail', kwargs={'pk': self.subject.pk})

    def form_valid(self, form):
        """
        Display a success message.
        """
        messages.success(self.request, _('Document uploaded successfully.'))
        return super().form_valid(form)


class DocumentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a document.
    """
    model = Document
    template_name = 'subjects/document_confirm_delete.html'

    def test_func(self):
        """
        Ensure the document belongs to the current user.
        """
        document = self.get_object()
        return document.subject.user == self.request.user

    def get_success_url(self):
        """
        Return to the subject detail page.
        """
        return reverse('subject_detail', kwargs={'pk': self.object.subject.pk})

    def delete(self, request, *args, **kwargs):
        """
        Display a success message.
        """
        messages.success(request, _('Document deleted successfully.'))
        return super().delete(request, *args, **kwargs)
