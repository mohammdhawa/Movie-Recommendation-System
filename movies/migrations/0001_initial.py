# Generated by Django 5.0.6 on 2024-05-23 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='actors/')),
                ('image_url', models.URLField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('production_country', models.CharField(max_length=255)),
                ('director', models.CharField(max_length=255)),
                ('runtime', models.IntegerField()),
                ('release_date', models.DateField()),
                ('language', models.CharField(max_length=255)),
                ('vote_average', models.FloatField()),
                ('vote_count', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='movies/')),
                ('trailer', models.URLField(blank=True, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('movie_id', models.IntegerField(blank=True, null=True)),
                ('tmdb_id', models.IntegerField(blank=True, null=True)),
                ('imdb_id', models.IntegerField(blank=True, null=True)),
                ('actors', models.ManyToManyField(related_name='movie_actors', to='movies.actor')),
                ('genres', models.ManyToManyField(related_name='movie_genres', to='movies.genre')),
            ],
        ),
    ]