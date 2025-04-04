from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('consumer', 'Consumer'),
        ('dealer', 'Dealer'),
        ('admin', 'Admin'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='consumer')

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

