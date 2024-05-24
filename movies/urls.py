from django.urls import path
from .views import search, MovieDetailView


urlpatterns = [
    path('search/', search, name='search'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
]