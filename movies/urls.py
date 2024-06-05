from django.urls import path
from .views import search, MovieDetailView, home


urlpatterns = [
    path('search/', search, name='search'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    # path('', MovieListView.as_view(), name='movie_list'),
    path('', home, name='home'),
]