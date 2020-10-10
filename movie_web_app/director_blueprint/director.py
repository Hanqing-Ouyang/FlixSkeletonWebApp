from flask import Blueprint, render_template, url_for, request

from flask_paginate import Pagination
from flask_paginate import Pagination, get_page_parameter
from movie_web_app.domainmodel.read_title import read_title

import movie_web_app.adapters.repository as repo


director_blueprint = Blueprint(
    'director_bp', __name__
)


@director_blueprint.route('/directors')
def list_director():
    return render_template(
        'others/list_director.html',
        home_url=url_for('home_bp.home'),
        list_movie_url=url_for('movie_bp.movies_by_year'),
        list_actor_url=url_for('actor_bp.list_actor'),
        list_director_url=url_for('director_bp.list_director'),
        list_genre_url=url_for('genre_bp.list_genre'),
        search_url=url_for('search_bp.find_movie'),
        register_url=url_for('authentication_bp.register'),
        directors=repo.repo_instance.get_directors()
    )

