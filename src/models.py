from flask_sqlalchemy import SQLAlchemy
from flask import g
from passlib.hash import sha256_crypt
from datetime import datetime as dt
from flask_migrate import Migrate
from . import app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    symbol = db.Column(db.String(16))
    exchange = db.Column(db.String(256))
    description = db.Column(db.String(1024))
    portfolio_id = db.Column(db.ForeignKey('portfolios.id'), nullable=False)

    portfolio = db.relationship('Portfolio', back_populates='companies', lazy=True)


class Portfolio(db.Model):
    __tablename__ = 'portfolios'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=dt.now())
    user_id = db.Column(db.ForeignKey('users.id'), nullable=False)

    companies = db.relationship('Company', back_populates='portfolio', lazy=True)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=dt.now())

    portfolios = db.relationship('Portfolio', backref='user', lazy=True)

    def __init__(self, email, raw_pass):
        self.email = email
        self.password = sha256_crypt.hash(raw_pass)

    @classmethod
    def check_password_hash(cls, user, raw_pass):
        if user is not None:
            if sha256_crypt.verify(raw_pass, user.password):
                return True

        return False
