from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='players')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Team(models.Model):
    city = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')

    def __str__(self):
        return f"{self.city} {self.nickname}"
