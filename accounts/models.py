from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='user.png', upload_to='users', blank=True, null=True)
    watched_movies = models.ManyToManyField(Movie, related_name='watched_by', blank=True)

    def __str__(self):
        return str(self.user)
