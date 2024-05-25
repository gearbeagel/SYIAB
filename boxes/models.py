from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Box(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_opening = models.DateTimeField()

    def __str__(self):
        return self.name


class Component(models.Model):
    class ContentType(models.TextChoices):
        TEXT = 'T', _("Text")
        IMAGE = 'I', _("Image")
        VIDEO = 'V', _("Video")
        AUDIO = 'A', _("Audio")
        FILE = 'F', _("File")

    name = models.CharField(max_length=100)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    content_type = models.CharField(choices=ContentType.choices, max_length=1, default=ContentType.TEXT)

    def __str__(self):
        return f"{self.name}({self.content_type})"
