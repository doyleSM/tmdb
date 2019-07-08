from django.db import models
from django.contrib.auth.models import User


class Playlist(models.Model):
    name = models.CharField(max_length=50, default="no name")
    user = models.ForeignKey(User, on_delete="CASCADE")

    def __str__(self):
        return self.name
