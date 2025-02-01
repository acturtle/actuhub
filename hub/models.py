import os
import re

from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class CashFlowModel(models.Model):
    name = models.CharField(max_length=100)
    repository_url = models.URLField(verbose_name="Repository URL")
    description = models.TextField()

    def __str__(self):
        return self.name


def validate_version(value):
    # Allow blank values
    if not value:
        return
    # Regex for allowed characters: integers, :, -, commas, and spaces
    if not re.match(r'^[0-9:, -]*$', value):
        raise ValidationError(
            "Version can only contain integers, ':', '-', ',', spaces, or be blank."
        )


class Run(models.Model):
    cash_flow_model = models.ForeignKey(CashFlowModel, on_delete=models.CASCADE)
    version = models.CharField(
        max_length=100,
        blank=True,
        validators=[validate_version]
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('running', 'Running'),
            ('error', 'Error'),
            ('completed', 'Completed'),
        ),
        default='pending'
    )

    def __str__(self):
        return f"{self.cash_flow_model.name} - Version: {self.version}, Status: {self.status}"


def document_upload_path(instance, filename):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return os.path.join("documents", timestamp, filename)


class Document(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(
        upload_to=document_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf'],
                message="Only PDF files are allowed."
            )
        ]
    )
    cash_flow_models = models.ManyToManyField(CashFlowModel, blank=True)

    def __str__(self):
        return self.name
