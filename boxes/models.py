from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Box(models.Model):
    class Statuses(models.TextChoices):
        EDITED = 'E', _('Edited')
        LOCKED = 'L', _('Locked')
        OPENED = 'O', _('Opened')

    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_opening = models.DateTimeField()
    status = models.CharField(choices=Statuses.choices, default=Statuses.EDITED, max_length=100)

    def __str__(self):
        return self.name


class Memory(models.Model):
    class ContentType(models.TextChoices):
        TEXT = 'T', _("Text")
        IMAGE = 'I', _("Image")
        VIDEO = 'V', _("Video")
        AUDIO = 'A', _("Audio")
        FILE = 'F', _("File")

    name = models.CharField(max_length=100)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    content_type = models.CharField(choices=ContentType.choices, max_length=1, default=ContentType.TEXT)
    description = models.TextField()
    text_content = models.TextField(blank=True, null=True)
    image_content = models.ImageField(upload_to='images/', blank=True, null=True)
    video_content = models.FileField(upload_to='videos/', blank=True, null=True)
    audio_content = models.FileField(upload_to='audios/', blank=True, null=True)
    file_content = models.FileField(upload_to='files/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}({self.content_type})"
