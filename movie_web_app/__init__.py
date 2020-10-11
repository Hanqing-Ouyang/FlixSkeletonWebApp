from flask import Flask, request, url_for
from typing import List
import os
import movie_web_app.adapters.repository as repo
import movie_web_app.adapters.movie_repository as mv_repo

from movie_web_app.domainmodel import model
from movie_web_app.domainmodel.user import User
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie_web_app.domainmodel.read_title import read_title


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = os.path.join('movie_web_app', 'datafiles')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    with app.app_context():
        from .movie_blueprint import movie
        app.register_blueprint(movie.movie_blueprint)

        from .home_blueprint import home
        app.register_blueprint(home.home_blueprint)

        from .actor_blueprint import actor
        app.register_blueprint(actor.actor_blueprint)

        from .director_blueprint import director
        app.register_blueprint(director.director_blueprint)

        from .genre_blueprint import genre
        app.register_blueprint(genre.genre_blueprint)

        from .search_blueprint import search
        app.register_blueprint(search.search_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    filename = 'movie_web_app/datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)
    repo.repo_instance = mv_repo.MainRepository()
    repo.repo_instance.add_movies(movie_file_reader.dataset_of_movies)
    repo.repo_instance.add_actors(movie_file_reader.dataset_of_actors)
    repo.repo_instance.add_directors(movie_file_reader.dataset_of_directors)
    repo.repo_instance.add_genres(movie_file_reader.dataset_of_genres)
    mv_repo.populate(data_path, repo.repo_instance)

    return app
