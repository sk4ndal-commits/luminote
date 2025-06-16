from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

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
