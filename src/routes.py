from flask import render_template, abort, redirect, url_for, request
from sqlalchemy.exc import DBAPIError, IntegrityError
from .models import db, Company
from . import app
import requests
import json
import os


@app.route('/')
def home():
    return render_template('home.html'), 200


@app.route('/search', methods=['GET'])
def search():
    return render_template('search.html'), 200


@app.route('/search', methods=['POST'])
def search_results():
    symbol = request.form.get('symbol')
    url = 'https://api.iextrading.com/1.0/stock/{}/company'.format(symbol)
    res = requests.get(url)
    data = json.loads(res.text)
    try:
        company = Company(
            name=data['companyName'],
            symbol=data['symbol'],
            exchange=data['exchange'],
            description=data['description']
        )
        db.session.add(company)
        db.session.commit()
    except (DBAPIError, IntegrityError):
        abort(400)
    return redirect(url_for('.portfolio'), code=302)


@app.route('/portfolio', methods=['GET'])
def portfolio():
    companies = Company.query.all()
    return render_template('portfolio.html', companies=companies), 200
