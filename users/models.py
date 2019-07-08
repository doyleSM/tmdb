from django.db import models

# Create your models here.


class Registered(models.Model):
    chat_id = models.CharField(max_length=50)

    def __str__(self):
        return self.chat_id
