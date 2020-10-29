from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from movie_web_app.domainmodel import director
from movie_web_app.domainmodel import actor
from movie_web_app.domainmodel import genre
from movie_web_app.domainmodel import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('year', Integer, nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(255), nullable=True),
    Column('director', String(255), nullable=True),
    Column('actors', String(1024), nullable=True),
    Column('genres', String(255), nullable=True),
    Column('reviews', String(255), nullable=True)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id'))
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('director_full_name', String(64), nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_full_name', String(64), nullable=False)
)




def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Review, reviews, properties={
        '_review': reviews.c.review,
        '_timestamp': reviews.c.timestamp
    })
    movies_mapper = mapper(model.Movie, movies, properties={
        '_id': movies.c.id,
        '_year': movies.c.year,
        '_title': movies.c.title,
        '_reviews': relationship(model.Review, backref='_movie'),
    })
    mapper(genre.Genre, genres, properties={
        '_genre_name': genres.c.name,
        '_genreged_movies': relationship(
            movies_mapper,
            secondary=movie_genres,
            backref="_genres"
        )
    })