from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Subject

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