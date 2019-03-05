from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CompanyForm(FlaskForm):
    symbol = StringField('Symbol: ', validators=[DataRequired()])


class CompanyAddForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    symbol = StringField('symbol', validators=[DataRequired()])
    exchange = StringField('exchange', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
