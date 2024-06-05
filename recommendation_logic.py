import pandas as pd
import pickle
import requests

# import django
# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject1.settings')
# django.setup()

path = "content_based.pkl"

# Load data from pickle file
with open(path, 'rb') as f:
    data = pickle.load(f)

with open('actors_ids.pkl', 'rb') as f:
    actors_data = pickle.load(f)

# Access loaded data
actors_ids = actors_data['actors_ids']
movies_ = data['movies']
movies_filter_content_based = data['movies_filter_content_based']
final_movies = data['final_movies']


# Define the recommend_movies4 function
def recommend_movies4(movie_title):
    movie_id = movies_filter_content_based.loc[movies_filter_content_based['title'] == movie_title, 'id'].values
    movie_id = movie_id[0]

    movie_row = movies_filter_content_based[movies_filter_content_based['id'] == movie_id]

    if movie_row.empty:
        raise RuntimeError(f"Couldn't find any movie with ID: {movie_id}")

    movie_row = movie_row.iloc[0]

    director = movie_row['movie_director']
    actors = [movie_row[f'actor_{i}'] for i in range(1, 4)]
    genres = [movie_row[f'genre_{i}'] for i in range(1, 4)]

    keywords = [movie_row[f'keyword_{i}'] for i in range(1, 6)]
    rec_df = movies_filter_content_based.copy()

    rec_df['same_director'] = (rec_df['movie_director'] == director).astype(int)

    for i, actor in enumerate(actors):
        rec_df[f'same_a{i + 1}'] = ((rec_df['actor_1'] == actor) |
                                    (rec_df['actor_2'] == actor) |
                                    (rec_df['actor_3'] == actor)).astype(int)

    for i, genre in enumerate(genres):
        rec_df[f'same_g{i + 1}'] = ((rec_df['genre_1'] == genre) |
                                    (rec_df['genre_2'] == genre) |
                                    (rec_df['genre_3'] == genre)).astype(int)

    for i, keyword in enumerate(keywords):
        rec_df[f'same_k{i + 1}'] = ((rec_df['keyword_1'] == keyword) |
                                    (rec_df['keyword_2'] == keyword) |
                                    (rec_df['keyword_3'] == keyword) |
                                    (rec_df['keyword_4'] == keyword) |
                                    (rec_df['keyword_5'] == keyword)).astype(int)

    rec_df.loc[:, 'same_director': 'same_k5'] = rec_df.loc[:, 'same_director': 'same_k5'].fillna(0)
    rec_df['sim_count'] = rec_df.loc[:, 'same_director': 'same_k5'].sum(axis=1)
    rec_df = rec_df.merge(movies_[['id', 'weighted_rating']], on='id')

    # Select top 5 recommended movies based on similarity count and weighted rating
    top5_rec = rec_df.sort_values(by=['sim_count', 'weighted_rating'], ascending=[False, False]).iloc[:5]

    return list(top5_rec['id'])


def get_movie_detail(movie_id):
    result = final_movies[final_movies['id'] == movie_id]
    if not result.empty:
        return dict(result.iloc[0])
    else:
        return None


def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=2646356451a5c6c0d4606b0ccb8a0b0a&language=en-US")
    movie_poster = response.json()
    return "https://image.tmdb.org/t/p/w500/" + movie_poster['poster_path']


# Function to get actor_id by actor_name
def get_actor_id_by_name(name):
    result = actors_ids.loc[actors_ids['actor'] == name, 'actor_id']
    if not result.empty:
        return result.values[0]
    else:
        return None


def fetch_actor_profile(actor_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/person/{actor_id}/images?api_key=2646356451a5c6c0d4606b0ccb8a0b0a&language=en-US")
    actor_image = response.json()['profiles'][0]['file_path']
    return "https://image.tmdb.org/t/p/w500/" + actor_image

# mytest = recommend_movies4('Spider-Man')
# print(fetch_poster(mytest[0]))
# print(get_movie_detail(mytest[0]))
# print(mytest)
# print("Hello fucking world2")