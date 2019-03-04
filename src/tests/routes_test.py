from src import app
import pytest


def test_home_route():
    res = app.test_client().get('/')
    assert res.status_code == 200
    assert b'<h1>Welcome to your future!</h1>' in res.data


def test_search_route():
    res = app.test_client().get('/search')
    assert res.status_code == 200
    assert b'<h1>Search:</h1>' in res.data


def test_portfolio_route(session):
    res = app.test_client().get('/portfolio')
    assert res.status_code == 200
    assert b'<h1>Portfolio</h1>' in res.data


def test_search_route_post(session):
    res = app.test_client().post('/search', data={'symbol': 'FB'})
    assert res.status_code == 302


def test_search_route_post_redirect(session):
    res = app.test_client().post('/search', data={'symbol': 'GOOGL'}, follow_redirects=True)
    assert res.status_code == 200
    assert b'Alphabet Inc. (GOOGL)' in res.data
