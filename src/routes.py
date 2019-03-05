from flask import render_template, abort, redirect, url_for, request, flash, session
from sqlalchemy.exc import DBAPIError, IntegrityError
from .forms import CompanyForm, CompanyAddForm
from .models import db, Company
from . import app
import requests
import json
import os


@app.route('/')
def home():
    return render_template('home.html'), 200


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = CompanyForm()
    if form.validate_on_submit():
        symbol = request.form.get('symbol')
        url = 'https://api.iextrading.com/1.0/stock/{}/company'.format(symbol)
        res = requests.get(url)
        data = json.loads(res.text)
        session['context'] = data
        return redirect(url_for('.confirm_company'))

    return render_template('search.html', form=form)


@app.route('/company', methods=['GET', 'POST'])
def confirm_company():
    form_context = {
        'name': session['context']['companyName'],
        'symbol': session['context']['symbol'],
        'exchange': session['context']['exchange'],
        'description': session['context']['description'],
    }
    form = CompanyAddForm(**form_context)
    if form.validate_on_submit():
        try:
            company = Company(
                name=form.data['name'],
                symbol=form.data['symbol'],
                exchange=form.data['exchange'],
                description=form.data['description']
            )
            db.session.add(company)
            db.session.commit()
        except (DBAPIError, IntegrityError):
            flash('Something went wrong with your search.')
            return render_template('search.html', form=form), 200

        return redirect(url_for('.portfolio'))

    return render_template(
        'company.html',
        form=form,
        **form_context
    )


@app.route('/portfolio', methods=['GET'])
def portfolio():
    companies = Company.query.all()
    return render_template('portfolio.html', companies=companies), 200
