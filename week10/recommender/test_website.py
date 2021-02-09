from flask.globals import request
import pytest
from website import app, get_movie

@pytest.fixture
def client():
    """Start the fake server"""
    with app.test_client() as client:
        yield client

def test_main_page(client):
    response = client.get('/')
    assert 'Movie' in response.data.decode('UTF-8')

def test_result_page(client):
    response = client.get('/recommender')
    assert 'Recommendations' in response.data.decode('UTF-8')