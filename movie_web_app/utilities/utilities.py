from flask import Blueprint, request, render_template, redirect, url_for, session

import movie_web_app.adapters.repository as repo
import movie_web_app.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


# def get_tags_and_urls():
#     genre_names = services.get_genre_names(repo.repo_instance)
#     genre_urls = dict()
#     for genre_name in genre_names:
#         genre_urls[genre_name] = url_for('news_bp.movies_by_genre', tag=genre_name)
#
#     return genre_urls


def get_selected_movies(quantity=3):
    articles = services.get_random_movies(quantity, repo.repo_instance)

    for article in articles:
        article['hyperlink'] = url_for('news_bp.articles_by_date', date=article['date'].isoformat())
    return articles
