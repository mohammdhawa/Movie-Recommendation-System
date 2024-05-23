import os
import requests
from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genres = models.ManyToManyField('Genre', related_name='movie_genres')
    production_country = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    runtime = models.IntegerField()
    release_date = models.DateField()
    language = models.CharField(max_length=255)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    image = models.ImageField(upload_to='movies/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # New field to store the URL of the image
    actors = models.ManyToManyField('Actor', related_name='movie_actors')
    trailer = models.URLField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)

    movie_id = models.IntegerField(blank=True, null=True)
    tmdb_id = models.IntegerField(blank=True, null=True)
    imdb_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save_image_from_url(self):
        if self.image_url:
            response = requests.get(self.image_url)
            if response.status_code == 200:
                # Save the downloaded image to the media directory
                media_root = settings.MEDIA_ROOT
                image_name = os.path.basename(self.image_url)
                image_path = os.path.join(media_root, "movies", image_name)
                with open(image_path, "wb") as f:
                    f.write(response.content)

                # Set the image field to the path of the saved image
                self.image = os.path.join("movies", image_name)

                # Save the model
                self.save()

                return True
        return False



class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='actors/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  # New field to store the URL of the image

    def __str__(self):
        return self.name

    def save_image_from_url(self):
        if self.image_url:
            response = requests.get(self.image_url)
            if response.status_code == 200:
                # Save the downloaded image to the media directory
                media_root = settings.MEDIA_ROOT
                image_name = os.path.basename(self.image_url)
                image_path = os.path.join(media_root, "actors", image_name)
                with open(image_path, "wb") as f:
                    f.write(response.content)

                # Set the image field to the path of the saved image
                self.image = os.path.join("actors", image_name)

                # Save the model
                self.save()

                return True
        return False
