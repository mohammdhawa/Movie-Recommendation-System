from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Movie, Actor, Genre
from recommendation_logic import (recommend_movies4, fetch_poster,
                                  get_movie_detail, get_actor_id_by_name,
                                  fetch_actor_profile)
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.urls import reverse
from accounts.models import Profile
from collaborative_recommendation_logic import recommended_for_you


# class MovieListView(ListView):
#     model = Movie
#     template_name = 'movies/index.html'
#
#     def get_queryset(self):
#         # Retrieve only the first 10 movies
#         return Movie.objects.all().order_by('-vote_average')[:3]
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["last_movies"] = Movie.objects.all().order_by('-release_date')[:6]
#         context['top_rated'] = Movie.objects.all().order_by('-vote_average')[:6]
#         return context


def home(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        user_id = profile.get_user_id_from_dataset
        for_user = recommended_for_you(user_id)
    else:
        for_user = None

    movies = Movie.objects.all()
    last_movies = movies.order_by('-release_date')[:6]
    top_movies = movies.order_by('-vote_average')[:6]
    object_list = movies.order_by('-vote_average')[:3]

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')

    context = {
        'last_movies': last_movies,
        'top_rated': top_movies,
        'object_list': object_list,
    }
    if for_user is not None:
        context['for_user'] = for_user

    return render(request, 'movies/index.html', context)


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movies/movie_details.html'


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        object_list = []
        recommended_list = recommend_movies4(searched)
        if recommended_list:
            for movie_id in recommended_list:
                try:
                    result = Movie.objects.get(tmdb_id=movie_id)

                    movie_actors = []
                    movie_genres = []
                    movie_detail = get_movie_detail(movie_id)
                    for i in range(1, 4):
                        if movie_detail[f"actor_{i}"]:
                            actor_name = movie_detail[f"actor_{i}"]
                            actor, created = Actor.objects.get_or_create(name=actor_name, defaults={
                                'image_url': fetch_actor_profile(get_actor_id_by_name(actor_name))})
                            if created:
                                actor.save_image_from_url()
                            movie_actors.append(actor)
                        if movie_detail[f"genre_{i}"]:
                            genre_name = movie_detail[f"genre_{i}"]
                            genre, created = Genre.objects.get_or_create(name=genre_name)
                            movie_genres.append(genre)

                    result.actors.set(movie_actors)
                    result.genres.set(movie_genres)
                    object_list.append(result)
                except Movie.DoesNotExist:
                    movie_detail = get_movie_detail(movie_id)
                    movie_actors = []
                    movie_genres = []
                    for i in range(1, 4):
                        if movie_detail[f"actor_{i}"]:
                            actor_name = movie_detail[f"actor_{i}"]
                            actor, created = Actor.objects.get_or_create(name=actor_name, defaults={
                                'image_url': fetch_actor_profile(get_actor_id_by_name(actor_name))})
                            if created:
                                actor.save_image_from_url()
                            movie_actors.append(actor)
                        if movie_detail[f"genre_{i}"]:
                            genre_name = movie_detail[f"genre_{i}"]
                            genre, created = Genre.objects.get_or_create(name=genre_name)
                            movie_genres.append(genre)

                    movie_poster = fetch_poster(movie_id)
                    new_movie, created = Movie.objects.get_or_create(
                        title=movie_detail['title'],
                        production_country=', '.join(movie_detail['production_countries']),
                        director=movie_detail['movie_director'],
                        runtime=int(movie_detail['runtime']),
                        release_date=f"{movie_detail['release_date']}-01-01",
                        language=movie_detail['original_language'],
                        vote_average=movie_detail['vote_average'],
                        vote_count=movie_detail['vote_count'] // 1000,
                        overview=movie_detail['overview'],
                        image_url=movie_poster,
                        tmdb_id=movie_id
                    )
                    if created:
                        new_movie.actors.set(movie_actors)
                        new_movie.genres.set(movie_genres)
                        new_movie.save_image_from_url()

                    object_list.append(new_movie)

            return render(request, 'movies/search.html', {'object_list': object_list})
        else:
            print("Error while getting recommended movies")
            return render(request, 'movies/search.html', {'searched': searched})
    else:
        return render(request, 'movies/search.html', {})
