from typing import Iterable
import random

import movie_web_app.adapters.movie_repository as mv_repo
import movie_web_app.adapters.actor_repository as ac_repo
import movie_web_app.adapters.director_repository as dr_repo
import movie_web_app.adapters.genre_repository as gr_repo
from movie_web_app.adapters.repository import AbstractRepository
from movie_web_app.domainmodel.movie import Movie


def get_genre_names(repo: AbstractRepository):
    genres = repo.get_genres()
    genre_names = [genre.genre_name for genre in genres]

    return genre_names


def get_random_movies(quantity, repo: AbstractRepository):
    movie_count = repo.get_number_of_movies()

    if quantity >= movie_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = movie_count - 1

    # Pick distinct and random movies.
    random_ids = random.sample(range(1, movie_count), quantity)
    movies = repo.get_movies_by_id(random_ids)

    return movies_to_dict(movies)


# ============================================
# Functions to convert dicts to model entities
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'Released Year': movie.year,
        'title': movie.title,

    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]
