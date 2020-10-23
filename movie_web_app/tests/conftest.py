import os
import pytest

from movie_web_app import create_app
from movie_web_app.adapters.movie_repository import MainRepository
import movie_web_app.adapters.repository as repo
import movie_web_app.adapters.movie_repository as mv_repo
from movie_web_app.datafilereaders.movie_file_csv_reader import MovieFileCSVReader


# TEST_DATA_PATH = os.path.join('C:', os.sep, 'iCloud Drive', 'Documents', 'GitHub', 'FlixSkeletonWebApp','movie_web_app', 'tests', 'data')
#TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'iwar006', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')
TEST_DATA_PATH = '/Users/takesei/Documents/GitHub/FlixSkeletonWebApp/movie_web_app/tests/data'

@pytest.fixture
def in_movie_repo():
    filename = '/Users/takesei/Documents/GitHub/FlixSkeletonWebApp/movie_web_app/datafiles/Data1000Movies.csv'
    movie_file_reader = MovieFileCSVReader(filename)

    repo.repo_instance = mv_repo.MainRepository()

    repo.repo_instance.add_movies(movie_file_reader.dataset_of_movies)
    repo.repo_instance.add_actors(movie_file_reader.dataset_of_actors)
    repo.repo_instance.add_directors(movie_file_reader.dataset_of_directors)
    repo.repo_instance.add_genres(movie_file_reader.dataset_of_genres)

    mv_repo.populate(TEST_DATA_PATH, repo.repo_instance)

    return repo.repo_instance


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,  # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,  # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False,  # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='thorke', password='cLQ^C#oFXloS'):
        return self._client.post(
            'authentication/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
