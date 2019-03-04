from src import app
import pytest


def test_home_route():
    res = app.test_client().get('/')
    assert res.status_code == 200
    assert b'<h1>Welcome to your future!</h1>' in res.text
