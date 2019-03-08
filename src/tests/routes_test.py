from src import app
from flask import session
import pytest


def test_home_route():
    res = app.test_client().get('/')
    assert res.status_code == 200
    assert b'<h1>Welcome to your future!</h1>' in res.data


def test_search_route_get(session, auth_client):
    res = auth_client.get('/search')
    assert res.status_code == 200
    assert b'<h1>Search</h1>' in res.data


def test_portfolio_route(session, auth_client):
    res = auth_client.get('/portfolio')
    assert res.status_code == 200
    assert b'<h1>Portfolio</h1>' in res.data


def test_bad_route():
    res = app.test_client().get('/qqqqqqq')
    assert res.status_code == 404
    assert b'<h1>404 - Page Not Found</h1>' in res.data


def test_search_route_post():
    res = app.test_client().post(
        '/search',
        data={'symbol': 'FB'}
    )
    assert res.status_code == 302


def test_search_bad_symbol(session, auth_client):
    res = auth_client.post(
        '/search',
        data={'symbol': 'BS'}
    )
    assert b'No results from API' in res.data


def test_search_redirect(session, auth_client):
    res = auth_client.post(
        '/search',
        data={'symbol': 'FB'},
        follow_redirects=True
    )
    assert b'<h1>Add to Portfolio?</h1>' in res.data
    assert b'(FB)' in res.data
    assert res.status_code == 200


@pytest.mark.skip('Research this')
def test_company_confirm(session):
    data = {
        'name': 'Code Fellows',
        'symbol': 'CF',
        'exchange': 'Some Exchange',
        'description': 'Description text goes in here.'
    }
    session['context'] = data
    res = app.test_client().post(
        '/company',
        data=data,
        follow_redirects=True
    )
    assert b'<h1>Portfolio</h1>' in res.data


def test_registration_get(client):
    res = client.get('/register')
    assert res.status_code == 200
    assert b'<h1>Register</h1>' in res.data


def test_registration_redirect(client):
    res = client.post(
        '/register',
        data={'email': 'py@test.com', 'password': '12345'},
        follow_redirects=True
    )
    assert b'<h1>Login</h1>' in res.data
