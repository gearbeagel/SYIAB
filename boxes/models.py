from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def generate_unique_slug(model_instance, slug_field, slug_value):
    slug = slugify(slug_value)
    model_class = model_instance.__class__
    unique_slug = slug
    num = 1
    while model_class.objects.filter(**{slug_field: unique_slug}).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug


class Box(models.Model):
    class Statuses(models.TextChoices):
        EDITED = 'E', _('Edited')
        LOCKED = 'L', _('Locked')
        OPENED = 'O', _('Opened')

    class Categories(models.TextChoices):
        FAMILY = 'FA', _('Family')
        TRAVEL = 'TR', _('Travel')
        FRIENDS = 'FR', _('Friends')
        LOVE = 'LO', _('Love')
        HOBBY = 'HO', _('Hobby')
        OTHER = 'O', _('Other')

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_opening = models.DateTimeField()
    status = models.CharField(choices=Statuses.choices, default=Statuses.EDITED, max_length=100)
    category = models.CharField(choices=Categories.choices, default=Categories.OTHER, max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'slug', self.name)
        super().save(*args, **kwargs)


class Memory(models.Model):
    class ContentType(models.TextChoices):
        TEXT = 'T', _("Text")
        IMAGE = 'I', _("Image")
        VIDEO = 'V', _("Video")
        AUDIO = 'A', _("Audio")
        FILE = 'F', _("File")

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, 'slug', self.name)
        super().save(*args, **kwargs)
