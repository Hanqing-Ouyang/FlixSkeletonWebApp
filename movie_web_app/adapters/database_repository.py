import csv
import os

from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie_web_app.domainmodel.director import Director
from movie_web_app.domainmodel.actor import Actor
from movie_web_app.domainmodel.genre import Genre
from movie_web_app.domainmodel.model import User,Review,Movie,make_review
from movie_web_app.adapters.repository import AbstractRepository

genres = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(movie).filter(movie._id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies_by_year(self, target_year: int) -> List[Movie]:
        if target_year is None:
            movies = self._session_cm.session.query(Movie).all()
            return movies
        else:
            # Return movies matching target_year; return an empty list if there are no matches.
            movies = self._session_cm.session.query(Movie).filter(Movie.year == target_year).all()
            return movies

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_first_movie(self):
        movie = self._session_cm.session.query(Movie).first()
        return movie

    def get_last_movie(self):
        movie = self._session_cm.session.query(Movie).order_by(desc(Movie.id)).first()
        return movie

    def get_movies_by_id(self, id_list):
        movies = self._session_cm.session.query(Movie).filter(Movie.id.in_(id_list)).all()
        return movies

    def get_movie_ids_for_genre(self, genre_name: str):
        movie_ids = []

        # Use native SQL to retrieve movie ids, since there is no mapped class for the movie_genres table.
        row = self._session_cm.session.execute('SELECT id FROM genres WHERE name = :genre_name', {'genre_name': genre_name}).fetchone()

        if row is None:
            # No genre with the name genre_name - create an empty list.
            movie_ids = list()
        else:
            genre_id = row[0]

            # Retrieve movie ids of movies associated with the genre.
            movie_ids = self._session_cm.session.execute(
                    'SELECT movie_id FROM movie_genres WHERE genre_id = :genre_id ORDER BY movie_id ASC',
                    {'genre_id': genre_id}
            ).fetchall()
            movie_ids = [id[0] for id in movie_ids]

        return movie_ids

    def get_year_of_previous_movie(self, movie: Movie):
        result = None
        prev = self._session_cm.session.query(movie).filter(movie._year < movie.year).order_by(desc(movie._year)).first()

        if prev is not None:
            result = prev.year

        return result

    def get_year_of_next_movie(self, movie: Movie):
        result = None
        next = self._session_cm.session.query(movie).filter(movie._year > movie.year).order_by(asc(movie._year)).first()

        if next is not None:
            result = next.year

        return result

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()


    # the Functions doesn't have #

    def add_actors(self, actors: list):
        for actor in actors:
            with self._session_cm as scm:
                scm.session.add(actor)
                scm.commit()

    def add_genres(self, genres: list):
        for genre in genres:
            with self._session_cm as scm:
                scm.session.add(genre)
                scm.commit()

    def add_directors(self, directors: list):
        for director in directors:
            with self._session_cm as scm:
                scm.session.add(director)
                scm.commit()

    def get_movies(self):
        movies = self._session_cm.session.query(Movie).all()
        return movies

    def get_actors(self):
        actors = self._session_cm.session.query(Actor).all()
        return actors

    def get_directors(self):
        directors = self._session_cm.session.query(Director).all()
        return directors

    def get_result(self, title: str) -> list:
        title=title.title().strip()
        movies= self._session_cm.session.execute(
                    """SELECT movie 
                    FROM movies, 
                    WHERE movie.title = :title 
                    OR movie.actors.actor_full_name LIKE :title 
                    OR movie.director.director_full_name LIKE :title 
                    OR movie.genres.genre_name LIKE :title 
                    ORDER BY movie_id ASC""",
                    {'title': title }
            ).fetchall()
        return movies
        # for movie in self._movies:
        #     if movie.title == title or \
        #             Actor(title) in movie.actors or \
        #             movie.director == Director(title) or \
        #             Genre(title) in movie.genres:
        #         movies.append(movie)
        # return movies

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()
        # self._directors.append(director)

    def get_director(self, director_full_name: str):
        director = self._session_cm.session.query(Director).filter(Director.director_full_name == director_full_name).order_by(asc(Director.director_full_name)).first()
        return director
        # return next((director for director in self._directors if director.director_full_name == director_full_name), None)

    def add_actor(self, actor: Actor):
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()
        # self._actors.append(actor)

    def get_actor(self, actor_full_name: str):
        actor = self._session_cm.session.query(Actor).filter(
            Actor.actor_full_name == actor_full_name).order_by(asc(Actor.actor_full_name)).first()
        return actor
        # return next((actor for actor in self._actors if actor.actor_full_name == actor_full_name), None)

    def add_favorite_movie(self, user: User, movie: Movie):
        user.watch_movie(movie)
        if user in self._watchlist_dict.keys():
            if movie not in self._watchlist_dict.values():
                self._watchlist_dict[user].append(movie)

    def get_watchlist(self,user):
        return self._watchlist_dict[user]

    def add_movies(self, movies:list):
        for movie in movies:
            self._movies.append(movie)
            self._movies_index[movie.id] = movie
            if movie.year not in self._years:
                self._years.append(movie.year)

    def get_genre(self, genre_name) -> Genre:
        genre = self._session_cm.session.query(Genre).filter(Genre.genre_name == genre_name).one()
        return genre
        # return next((genre for genre in self._genres if genre.genre_name == genre_name), None)

    def get_users(self):
        users = self._session_cm.session.query(User).all()
        return users
        # return self._users

def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:

            movie_data = row
            movie_key = movie_data[0]

            # Strip any leading/trailing white space from data read.
            movie_data = [item.strip() for item in movie_data]

            number_of_genres = len(movie_data) - 6
            movie_genres = movie_data[-number_of_genres:]

            # Add any new genres; associate the current movie with genres.
            for genre in movie_genres:
                if genre not in genres.keys():
                    genres[genre] = list()
                genres[genre].append(movie_key)

            del movie_data[-number_of_genres:]

            yield movie_data


def get_genre_records():
    genre_records = list()
    genre_key = 0

    for genre in genres.keys():
        genre_key = genre_key + 1
        genre_records.append((genre_key, genre))
    return genre_records


def movie_genres_generator():
    movie_genres_key = 0
    genre_key = 0

    for genre in genres.keys():
        genre_key = genre_key + 1
        for movie_key in genres[genre]:
            movie_genres_key = movie_genres_key + 1
            yield movie_genres_key, movie_key, genre_key


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global genres
    genres = dict()

    insert_movies = """
        INSERT INTO movies (
        id, year, title)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'news_movies.csv')))

    insert_genres = """
        INSERT INTO genres (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_genres, get_genre_records())

    insert_movie_genres = """
        INSERT INTO movie_genres (
        id, movie_id, genre_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genres, movie_genres_generator())

    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_reviews = """
        INSERT INTO reviews (
        id, user_id, movie_id, review, timestamp)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_reviews, generic_generator(os.path.join(data_path, 'reviews.csv')))

    conn.commit()
    conn.close()