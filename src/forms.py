from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired
from .models import Portfolio


class CompanyForm(FlaskForm):
    symbol = StringField('Symbol: ', validators=[DataRequired()])


class CompanyAddForm(FlaskForm):
    name = StringField('Name: ', validators=[DataRequired()])
    symbol = StringField('Symbol: ', validators=[DataRequired()])
    exchange = StringField('Exchange: ', validators=[DataRequired()])
    description = StringField('Description: ', validators=[DataRequired()])
    portfolios = SelectField('Portfolio: ')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.portfolios.choices = [(str(c.id), c.name) for c in Portfolio.query.all()]


class PortfolioAddForm(FlaskForm):
    name = StringField('Portfolio Name: ', validators=[DataRequired()])


class AuthForm(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
