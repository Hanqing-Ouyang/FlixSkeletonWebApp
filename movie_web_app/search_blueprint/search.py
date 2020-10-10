from flask import Blueprint, render_template, url_for, request
from flask_wtf import FlaskForm
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
import movie_web_app.adapters.movie_repository as mv_repo

import movie_web_app.adapters.repository as repo
from wtforms import IntegerField, SubmitField ,StringField
from wtforms.validators import DataRequired


search_blueprint = Blueprint(
    'search_bp', __name__
)


@search_blueprint.route('/find', methods=['GET', 'POST'])
def find_movie():
    form = SearchForm()
    boolean = form.validate_on_submit()

    if boolean:
        posted_title = form.movie_title.data

        movie = repo.repo_instance.get_result(posted_title.title().strip())
        return render_template(
            'search/MovieResult.html',
            movies=movie,
            home_url=url_for('home_bp.home'),
            list_movie_url=url_for('movie_bp.movies_by_year'),
            list_actor_url=url_for('actor_bp.list_actor'),
            list_director_url=url_for('director_bp.list_director'),
            list_genre_url=url_for('genre_bp.list_genre'),
            search_url=url_for('search_bp.find_movie'),
            register_url=url_for('authentication_bp.register'),
        )
    return render_template(
        'search/SearchMovie.html',
        home_url=url_for('home_bp.home'),
        list_movie_url=url_for('movie_bp.movies_by_year'),
        list_actor_url=url_for('actor_bp.list_actor'),
        list_director_url=url_for('director_bp.list_director'),
        list_genre_url=url_for('genre_bp.list_genre'),
        search_url=url_for('search_bp.find_movie'),
        handler_url = url_for('search_bp.find_movie'),
        register_url=url_for('authentication_bp.register'),
        form=form,
    )

class SearchForm(FlaskForm):
    movie_title = StringField('Find your movie here by Movie Title/Actor/Director', [DataRequired(message='This field is required')])
    submit = SubmitField('Find')