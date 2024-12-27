from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):

    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
