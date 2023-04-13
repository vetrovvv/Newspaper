from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rate = models.IntegerField(null = True, blank=True)
