from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    # followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    following = models.ManyToManyField(
        "self",
        symmetrical=False,   # Important! A follows B doesn’t mean B follows A
        related_name="followers",
        blank=True
    )

    def __str__(self):
        return self.username
