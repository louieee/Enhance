from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')
