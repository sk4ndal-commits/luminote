# Generated manually

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subjects', '0002_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='uploaded_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='uploaded at'),
            preserve_default=False,
        ),
    ]