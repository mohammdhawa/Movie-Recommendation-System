from django.urls import path
from .views import search, MovieDetailView, home, imdb_top_rated


urlpatterns = [
    path('search/', search, name='search'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('top_imdb_movies/', imdb_top_rated, name='top_imdb_movies'),
    # path('', MovieListView.as_view(), name='movie_list'),
    path('', home, name='home'),
]