'''
Test suites for the Flask application.
'''
import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_login(client):
    error_msg = b'Please try again.'
    success_msg = b'You are logged in.'

    result = client.post(
        '/login',
        data={'username': 'notexists', 'password': 'foo'},
        follow_redirects=True
    )
    assert error_msg in result.data

    result = client.post(
        '/login',
        data={'username': 'suefrank1234', 'password': 'incorrect'},
        follow_redirects=True
    )
    assert error_msg in result.data

    result = client.post(
        '/login',
        data={'username': 'suefrank1234', 'password': 'lightbulb'},
        follow_redirects=True
    )
    assert success_msg in result.data


def test_greeting(client):
    result = client.post(
        '/login',
        data={'username': 'suefrank1234', 'password': 'lightbulb'},
        follow_redirects=True
    )
    assert b'suefrank' in result.data


def test_logout(client):
    greeting = b'You are logged in.'
    client.post(
        '/login',
        data={'username': 'suefrank1234', 'password': 'lightbulb'},
        follow_redirects=True
    )

    result = client.get('/logout')
    assert greeting not in result.data
