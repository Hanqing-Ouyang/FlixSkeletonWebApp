from flask import Blueprint, render_template, url_for, request

from flask_paginate import Pagination
from flask_paginate import Pagination, get_page_parameter
from movie_web_app.domainmodel.read_title import read_title

import movie_web_app.adapters.repository as repo


actor_blueprint = Blueprint(
    'actor_bp', __name__
)


@actor_blueprint.route('/actors')
def list_actor():
    actors = repo.repo_instance.get_actors()
    per_page = 50
    a=1
    actor_list = []
    actor_index =[]
    for actor in actors:
        actor_list.append(actor)
        actor_index.append(a)
        a+=1
    total = len(actor_list)
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page
    pagination2 = Pagination(bs_version=3, page=page, total=total)
    actor_per_page = actor_list[start:end]


    return render_template(
        'others/list_actor.html',
        home_url=url_for('home_bp.home'),
        list_movie_url=url_for('movie_bp.movies_by_year'),
        list_actor_url=url_for('actor_bp.list_actor'),
        list_director_url=url_for('director_bp.list_director'),
        list_genre_url=url_for('genre_bp.list_genre'),
        search_url=url_for('search_bp.find_movie'),
        register_url= url_for('authentication_bp.register'),
        actors=actor_per_page,
        ids=actor_index,
        pagination=pagination2
    )