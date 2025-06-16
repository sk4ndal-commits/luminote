import os
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class Subject(models.Model):
    """
    Subject model for organizing materials by course.
    """
    name = models.CharField(_('name'), max_length=100)
    description = models.TextField(_('description'), blank=True)
    tags = models.CharField(_('tags'), max_length=255, blank=True, help_text=_('Comma-separated tags'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name=_('user')
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('subject')
        verbose_name_plural = _('subjects')
        ordering = ['-created_at']

    def __str__(self):
        return self.name


def document_file_path(instance, filename):
    """
    Generate file path for new document.
    Format: documents/user_id/subject_id/filename
    """
    return f'documents/{instance.subject.user.id}/{instance.subject.id}/{filename}'


class Document(models.Model):
    """
    Document model for storing uploaded files with metadata.
    """
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('subject')
    )
    title = models.CharField(_('title'), max_length=255)
    file = models.FileField(
        _('file'),
        upload_to=document_file_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx'])]
    )
    file_type = models.CharField(_('file type'), max_length=10)
    file_size = models.PositiveIntegerField(_('file size'), help_text=_('Size in bytes'))
    page_count = models.PositiveIntegerField(_('page count'), null=True, blank=True)
    uploaded_at = models.DateTimeField(_('uploaded at'), auto_now_add=True)

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Set file type based on extension
        if self.file:
            _, ext = os.path.splitext(self.file.name)
            self.file_type = ext.lower().lstrip('.')

            # Set file size
            if hasattr(self.file, 'size'):
                self.file_size = self.file.size

        super().save(*args, **kwargs)
