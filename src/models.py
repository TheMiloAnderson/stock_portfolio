from flask_sqlalchemy import SQLAlchemy
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

    companies = db.relationship('Company', back_populates='portfolio', lazy=True)
