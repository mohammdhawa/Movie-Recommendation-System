from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='users/user.png', upload_to='users', blank=True, null=True)
    watched_movies = models.ManyToManyField(Movie, related_name='watched_by', blank=True)
    get_user_id_from_dataset = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user)


# Create new user ---> create new empty profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
