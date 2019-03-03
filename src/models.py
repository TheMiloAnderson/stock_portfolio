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

    def __repr__(self):
        return {
            'name': self.name,
            'symbol': self.symbol,
            'exchange': self.exchange,
            'description': self.description
        }
