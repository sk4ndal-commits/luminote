from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Subject, Topic, Document
from .forms import SubjectForm, TopicForm, DocumentForm

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
        Add documents and topics to context.
        """
        context = super().get_context_data(**kwargs)
        context['topics'] = self.object.topics.all().order_by('name')

        # Get documents without a topic
        context['general_documents'] = self.object.documents.filter(topic__isnull=True).order_by('-uploaded_at')

        # Get documents organized by topic
        topic_documents = {}
        for topic in context['topics']:
            topic_documents[topic.id] = topic.documents.all().order_by('-uploaded_at')
        context['topic_documents'] = topic_documents

        # Keep the original documents list for backward compatibility
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


class TopicCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View for creating a new topic within a subject.
    """
    model = Topic
    form_class = TopicForm
    template_name = 'subjects/topic_form.html'

    def setup(self, request, *args, **kwargs):
        """
        Set up the view with the subject.
        """
        super().setup(request, *args, **kwargs)
        self.subject = get_object_or_404(Subject, pk=self.kwargs['subject_pk'])

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
        Redirect to the subject detail page after creation.
        """
        return reverse('subject_detail', kwargs={'pk': self.subject.pk})

    def form_valid(self, form):
        """
        Add success message after creation.
        """
        messages.success(self.request, _('Topic created successfully.'))
        return super().form_valid(form)


class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View for updating a topic.
    """
    model = Topic
    form_class = TopicForm
    template_name = 'subjects/topic_form.html'
    context_object_name = 'topic'

    def test_func(self):
        """
        Ensure the topic belongs to the current user.
        """
        topic = self.get_object()
        return topic.subject.user == self.request.user

    def get_context_data(self, **kwargs):
        """
        Add subject to context.
        """
        context = super().get_context_data(**kwargs)
        context['subject'] = self.object.subject
        return context

    def get_success_url(self):
        """
        Redirect to the subject detail page after update.
        """
        return reverse('subject_detail', kwargs={'pk': self.object.subject.pk})

    def form_valid(self, form):
        """
        Add success message after update.
        """
        messages.success(self.request, _('Topic updated successfully.'))
        return super().form_valid(form)


class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    View for deleting a topic.
    """
    model = Topic
    template_name = 'subjects/topic_confirm_delete.html'
    context_object_name = 'topic'

    def test_func(self):
        """
        Ensure the topic belongs to the current user.
        """
        topic = self.get_object()
        return topic.subject.user == self.request.user

    def get_success_url(self):
        """
        Redirect to the subject detail page after deletion.
        """
        return reverse('subject_detail', kwargs={'pk': self.object.subject.pk})

    def delete(self, request, *args, **kwargs):
        """
        Add success message after deletion.
        """
        topic = self.get_object()
        messages.success(request, _('Topic deleted successfully.'))
        return super().delete(request, *args, **kwargs)


class DocumentListView(LoginRequiredMixin, ListView):
    """
    View for displaying a list of documents belonging to the current user.
    """
    model = Document
    template_name = 'subjects/document_list.html'
    context_object_name = 'documents'

    def get_queryset(self):
        """
        Return only documents belonging to the current user.
        Filter by document type if specified in the query parameters.
        """
        queryset = Document.objects.filter(subject__user=self.request.user).order_by('-uploaded_at')

        # Filter by document type if specified
        document_type = self.request.GET.get('type')
        if document_type in dict(Document.DOCUMENT_TYPES):
            queryset = queryset.filter(document_type=document_type)

        # Filter by subject if specified
        subject_id = self.request.GET.get('subject')
        if subject_id and subject_id.isdigit():
            queryset = queryset.filter(subject_id=subject_id)

            # Filter by topic if specified
            topic_id = self.request.GET.get('topic')
            if topic_id == 'none':
                queryset = queryset.filter(topic__isnull=True)
            elif topic_id and topic_id.isdigit():
                queryset = queryset.filter(topic_id=topic_id)

        # Search by title if specified
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(topic__name__icontains=search_query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add subjects, topics, and filters to context.
        """
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.filter(user=self.request.user)
        context['document_types'] = Document.DOCUMENT_TYPES

        # Add current filters to context
        context['current_type'] = self.request.GET.get('type', '')
        context['current_subject'] = self.request.GET.get('subject', '')
        context['current_topic'] = self.request.GET.get('topic', '')
        context['current_search'] = self.request.GET.get('q', '')

        # Add topics for the selected subject
        if context['current_subject'] and context['current_subject'].isdigit():
            context['topics'] = Topic.objects.filter(
                subject_id=context['current_subject']
            ).order_by('name')
        else:
            context['topics'] = []

        return context


class DocumentUploadFromListView(LoginRequiredMixin, CreateView):
    """
    View for uploading documents from the document list view.
    """
    model = Document
    template_name = 'subjects/document_form_from_list.html'
    form_class = DocumentForm
    success_url = reverse_lazy('document_list')

    def get_form_class(self):
        """
        Return the form class to use.
        """
        return DocumentForm

    def get_form_kwargs(self):
        """
        Pass the subject to the form if specified in the query parameters.
        """
        kwargs = super().get_form_kwargs()
        subject_id = self.request.GET.get('subject')
        if subject_id and subject_id.isdigit():
            subject = get_object_or_404(Subject, pk=subject_id, user=self.request.user)
            kwargs['subject'] = subject
        return kwargs

    def get_context_data(self, **kwargs):
        """
        Add subjects to context.
        """
        context = super().get_context_data(**kwargs)
        context['subjects'] = Subject.objects.filter(user=self.request.user)
        subject_id = self.request.GET.get('subject')
        if subject_id and subject_id.isdigit():
            context['selected_subject'] = get_object_or_404(Subject, pk=subject_id, user=self.request.user)
        return context

    def form_valid(self, form):
        """
        Set the subject and display a success message.
        """
        # If subject is not set in the form, get it from the POST data
        if not hasattr(form.instance, 'subject') or not form.instance.subject:
            subject_id = self.request.POST.get('subject')
            if subject_id and subject_id.isdigit():
                subject = get_object_or_404(Subject, pk=subject_id, user=self.request.user)
                form.instance.subject = subject
            else:
                form.add_error('subject', _('Please select a subject.'))
                return self.form_invalid(form)

        messages.success(self.request, _('Document uploaded successfully.'))
        return super().form_valid(form)
