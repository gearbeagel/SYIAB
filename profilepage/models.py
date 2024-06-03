from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class ProfilePicture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', default='profile_pictures'
                                                                              '/default_profile_picture.png')

    def __str__(self):
        return str(self.profile_picture)
