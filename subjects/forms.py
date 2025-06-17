from django import forms
from django.utils.translation import gettext_lazy as _
import PyPDF2
import docx
import io
import os
from .models import Subject, Document

class SubjectForm(forms.ModelForm):
    """
    Form for creating and editing subjects.
    """
    class Meta:
        model = Subject
        fields = ['name', 'description', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.TextInput(attrs={'placeholder': _('Enter comma-separated tags')}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.pk:  # Only set user on new instances
            instance.user = self.user
        if commit:
            instance.save()
        return instance


class DocumentForm(forms.ModelForm):
    """
    Form for uploading documents.
    """
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': _('Enter document title')}),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.subject = kwargs.pop('subject', None)
        super().__init__(*args, **kwargs)

    def clean_file(self):
        """
        Validate file type and extract metadata.
        """
        file = self.cleaned_data.get('file')
        if not file:
            return None

        # Check file extension
        _, ext = os.path.splitext(file.name)
        ext = ext.lower().lstrip('.')

        if ext not in ['pdf', 'docx']:
            raise forms.ValidationError(_('Only PDF and DOCX files are allowed.'))

        return file

    def save(self, commit=True):
        instance = super().save(commit=False)

        if self.subject:
            instance.subject = self.subject

        # Extract metadata from the file
        file = self.cleaned_data.get('file')
        if file:
            # Get file size
            instance.file_size = file.size

            # Get file type
            _, ext = os.path.splitext(file.name)
            instance.file_type = ext.lower().lstrip('.')

            # Get page count
            try:
                if instance.file_type == 'pdf':
                    # Reset file pointer to beginning
                    file.seek(0)
                    reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
                    instance.page_count = len(reader.pages)
                elif instance.file_type == 'docx':
                    # Reset file pointer to beginning
                    file.seek(0)
                    doc = docx.Document(io.BytesIO(file.read()))
                    instance.page_count = len(doc.paragraphs)
            except Exception as e:
                # If we can't get page count, just leave it as None
                pass

            # Reset file pointer to beginning for saving
            file.seek(0)

        if commit:
            instance.save()

        return instance
