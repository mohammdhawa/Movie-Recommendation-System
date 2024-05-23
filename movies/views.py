from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Movie, Actor, Genre
from recommendation_logic import (recommend_movies4, fetch_poster,
                                  get_movie_detail, get_actor_id_by_name,
                                  fetch_actor_profile)
import random


class MovieListView(ListView):
    model = Movie
    template_name = 'movies/index.html'

    def get_queryset(self):
        # Retrieve only the first 10 movies
        return Movie.objects.all()[:10]


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        object_list = []
        print(searched)
        print(type(searched))
        recommended_list = recommend_movies4(searched)
        if recommended_list:
            print(recommended_list)
            for movie in recommended_list:
                movie_detail = get_movie_detail(movie)
                # movie_ = Movie.objects.get(title__iexact=)
                genres = Genre.objects.all()
                actors = Actor.objects.all()
                movie_ = Movie.objects.create(
                    title="mytest",
                    production_country="mytest",
                    director="mytest",
                    runtime=90,
                    release_date=1999,
                    language='en',
                    vote_average=4.7,
                    vote_count=4002,
                )
                movie_.genres.set(random.sample(genres, k=min(len(genres), 2)))
                movie_.actors.set(random.sample(actors, k=min(len(actors), 3)))
                movie_.save_image_from_url(fetch_poster(movie_detail['id']))
                print(movie)

                print(movie_detail)
                movie_detail['image'] = fetch_poster(movie_detail['id'])
                movie_detail['vote_count'] = movie_detail['vote_count'] // 1000
                name_1 = movie_detail['actor_1']
                name_2 = movie_detail['actor_2']
                name_3 = movie_detail['actor_3']
                actor_1_image = fetch_actor_profile(get_actor_id_by_name(movie_detail['actor_1']))
                actor_2_image = fetch_actor_profile(get_actor_id_by_name(movie_detail['actor_2']))
                actor_3_image = fetch_actor_profile(get_actor_id_by_name(movie_detail['actor_3']))

                object_list.append(movie_detail)
            return render(request, 'movies/search.html', {'object_list': object_list})
        else:
            print("Error while getting recommended movies")
            return render(request, 'movies/search.html', {'searched': searched})
    else:
        return render(request, 'movies/search.html', {})

