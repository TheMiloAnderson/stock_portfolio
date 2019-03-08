from src.models import db as _db
from src.models import Company, Portfolio, User
from src import app as _app
from flask import session as flask_session
import pytest
import os


@pytest.fixture()
def app(request):
    """ Session-wide testable Flask app """
    _app.config.from_mapping(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI=os.getenv('TEST_DATABASE_URL'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        WTF_CSRF_ENABLED=False
    )
    ctx = _app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return _app


@pytest.fixture()
def db(app, request):
    """ Session-wide test DB """
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture()
def session(db, request):
    """ Create new DB session for testing """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session


@pytest.fixture()
def client(app, db, session):
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client
    ctx.pop()


@pytest.fixture()
def user(session):
    user = User(
        email='test@pytest.com',
        raw_pass='12345'
    )
    session.add(user)
    session.commit()
    return user


@pytest.fixture()
def auth_client(client, user):
    client.post(
        '/login',
        data={'email': user.email, 'password': '12345'},
        follow_redirects=True
    )
    return client


@pytest.fixture()
def portfolio(session, user):
    portfolio = Portfolio(
        name='test_portfolio',
        user=user
    )
    session.add(portfolio)
    session.commit()
    return portfolio


@pytest.fixture()
def company(session, portfolio):
    company = Company(
        name='Code Fellows',
        symbol='CF',
        exchange='Some Exchange',
        description='We learn more faster',
        portfolio=portfolio
    )
    session.add(company)
    session.commit()
    return company
