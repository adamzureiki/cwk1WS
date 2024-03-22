from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length = 100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class News(models.Model):
    CHOICES_CAT = [
        ('pol', 'Politics'),
        ('art', 'Art'),
        ('tech', 'Technology'),
        ('trivia', 'Trivia'),
    ]
    CHOICES_REG = [
        ('uk', 'UK'),
        ('eu', 'European Union'),
        ('w', 'World'),
    ]
    headline = models.CharField(max_length=64)
    category = models.CharField(max_length=10, choices=CHOICES_CAT)
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=128)
    region = models.CharField(max_length=10, choices=CHOICES_REG )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
   