import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
django.setup()

import pickle
import requests
import pandas as pd
import numpy as np
from movies.models import Movie, Genre, Actor
from accounts.models import Profile
from recommendation_logic import fetch_actor_profile, fetch_poster

# Load data from collaborative_filtering.pkl file
path = "collaborative.pkl"
with open(path, 'rb') as f:
    data = pickle.load(f)

movies = data['movies']
actors = data['actors']
ratings = data['ratings']
best_svd_model = data['best_svd']
links = data['links']


def get_unseen_movies(user_id, ratings_df):
    seen_movies = ratings_df[ratings_df['userId'] == user_id]['movieId'].unique()
    all_movies = ratings_df['movieId'].unique()
    unseen_movies = np.setdiff1d(all_movies, seen_movies)
    return unseen_movies


def recommend_movies(user_id, model, ratings_df, top_n=10):
    unseen_movies = get_unseen_movies(user_id, ratings_df)
    predictions = []
    for movie_id in unseen_movies:
        prediction = model.predict(user_id, movie_id)
        predictions.append((movie_id, prediction.est))

    predictions.sort(key=lambda x: x[1], reverse=True)
    top_recommendations = predictions[:top_n]
    edited = [s[0] for s in top_recommendations]
    return edited


def get_tmdb_id_by_movieId(movie_id):
    result = links.loc[links['movieId'] == movie_id, 'tmdbId']
    if not result.empty:
        return result.values[0]
    else:
        return None


def watched_movies(user_id):
    user = ratings[ratings['userId'] == user_id]
    movies_list = []
    if not user.empty:
        for movie in user['movieId']:
            movies_list.append(movie)
        return movies_list
    else:
        return None


def helper(user_id, top_n=12):
    recommended = recommend_movies(user_id, best_svd_model, ratings, top_n=top_n)
    tmdb_ids = [get_tmdb_id_by_movieId(x) for x in recommended]
    return tmdb_ids


def recommended_for_you(user_id):
    movies_ids = helper(user_id)

    object_list = []

    for movie_id in movies_ids:
        try:
            movie = Movie.objects.get(tmdb_id=movie_id)
            movie_detail = get_movie_detail(movie_id)

            movie_actors = []
            movie_genres = []
            for i in range(1, 4):
                actor_detail = get_actor_detail(movie_detail[f"actor_{i}"])
                if actor_detail:
                    actor_name = actor_detail['name']
                    actor, created = Actor.objects.get_or_create(name=actor_name, defaults={
                        'image_url': fetch_actor_profile(actor_detail['id'])})
                    if created:
                        actor.save_image_from_url()
                    movie_actors.append(actor)
                if movie_detail[f"genre_{i}"]:
                    genre_name = movie_detail[f"genre_{i}"]
                    genre, created = Genre.objects.get_or_create(name=genre_name)
                    movie_genres.append(genre)

            movie.actors.set(movie_actors)
            movie.genres.set(movie_genres)
            object_list.append(movie)
        except Movie.DoesNotExist:
            movie = add_watched_movies_to_db(movie_id)
            object_list.append(movie)

    return object_list





def get_movie_detail(movie_id):
    result = movies[movies['id'] == movie_id]
    if not result.empty:
        return dict(result.iloc[0])
    else:
        return None


def get_actor_detail(actor_id):
    result = actors[actors['id'] == actor_id]
    if not result.empty:
        return dict(result.iloc[0])
    else:
        return None


def add_watched_movies_to_db(tmdb_id):
    movie_detail = get_movie_detail(tmdb_id)
    movie_actors = []
    movie_genres = []
    for i in range(1, 4):
        actor_detail = get_actor_detail(movie_detail[f"actor_{i}"])
        if actor_detail:
            actor_name = actor_detail['name']
            actor, created = Actor.objects.get_or_create(name=actor_name, defaults={
                'image_url': fetch_actor_profile(actor_detail['id'])})
            if created:
                actor.save_image_from_url()
            movie_actors.append(actor)
        if movie_detail[f"genre_{i}"]:
            genre_name = movie_detail[f"genre_{i}"]
            genre, created = Genre.objects.get_or_create(name=genre_name)
            movie_genres.append(genre)

    movie_poster = fetch_poster(tmdb_id)
    new_movie, created = Movie.objects.get_or_create(
        title=movie_detail['title'],
        production_country=movie_detail['production_countries'],
        director=movie_detail['director_name'],
        runtime=movie_detail['runtime'],
        release_date=f"{movie_detail['release_date']}",
        language=movie_detail['original_language'],
        vote_average=movie_detail['vote_average'],
        vote_count=int(movie_detail['vote_count']) // 1000,
        overview=movie_detail['overview'],
        image_url=movie_poster,
        tmdb_id=tmdb_id
    )
    if created:
        new_movie.actors.set(movie_actors)
        new_movie.genres.set(movie_genres)
        new_movie.save_image_from_url()

    return new_movie


def add_movies_to_user(user_id):
    print("User ID:", user_id)
    profile = Profile.objects.get(get_user_id_from_dataset=user_id)
    movies_list = watched_movies(user_id)
    if movies_list:
        watched_list = [get_tmdb_id_by_movieId(x) for x in movies_list]

    object_list = []
    if watched_list:
        for movie_id in watched_list:
            try:
                movie = Movie.objects.get(tmdb_id=movie_id)
                movie_detail = get_movie_detail(movie_id)

                movie_actors = []
                movie_genres = []
                for i in range(1, 4):
                    actor_detail = get_actor_detail(movie_detail[f"actor_{i}"])
                    if actor_detail:
                        actor_name = actor_detail['name']
                        actor, created = Actor.objects.get_or_create(name=actor_name, defaults={
                            'image_url': fetch_actor_profile(actor_detail['id'])})
                        if created:
                            actor.save_image_from_url()
                        movie_actors.append(actor)
                    if movie_detail[f"genre_{i}"]:
                        genre_name = movie_detail[f"genre_{i}"]
                        genre, created = Genre.objects.get_or_create(name=genre_name)
                        movie_genres.append(genre)

                movie.actors.set(movie_actors)
                movie.genres.set(movie_genres)
                object_list.append(movie)
            except Movie.DoesNotExist:
                movie = add_watched_movies_to_db(movie_id)
                object_list.append(movie)

        profile.watched_movies.set(object_list)


# add_movies_to_user(10)
