#accounts\models.py
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, max_length=500)

    def __str__(self):
        return f"{self.user.username}'s profile"
