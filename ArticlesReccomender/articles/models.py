from django.db import models
from django.contrib.auth.models import User


class User(User):
    id_t = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"


class Article(models.Model):
    title = models.CharField(max_length=1000, default='')
    doi = models.CharField(max_length=100)
    keywords = models.TextField(default='')
    url = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
