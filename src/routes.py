from flask import render_template, redirect, url_for, request, flash, session
from sqlalchemy.exc import DBAPIError, IntegrityError
from .forms import CompanyForm, CompanyAddForm, PortfolioAddForm
from .models import db, Company, Portfolio
from . import app
import requests
import json
import os


@app.add_template_global
def get_portfolios():
    return Portfolio.query.all()


@app.route('/')
def home():
    return render_template('home.html'), 200


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = CompanyForm()
    if form.validate_on_submit():
        try:
            symbol = request.form.get('symbol')
            url = 'https://api.iextrading.com/1.0/stock/{}/company'.format(
                symbol)
            res = requests.get(url)
            data = json.loads(res.text)
            session['context'] = data
            return redirect(url_for('.confirm_company'), code=302)
        except:
            flash('No results from API, check your symbol & try again')

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
                description=form.data['description'],
                portfolio_id=form.data['portfolios']
            )
            db.session.add(company)
            db.session.commit()
        except IntegrityError as e:
            # flash(form.data['name'] + ' is already in your Portfolios')
            flash(str(e.__cause__))
            return redirect(url_for('.confirm_company'))
        except DBAPIError as e:
            flash(str(e.__cause__))
            return redirect(url_for('.confirm_company'))

        return redirect(url_for('.portfolio'), code=302)

    return render_template(
        'company.html',
        form=form,
        **form_context
    )


@app.route('/portfolio', methods=['GET', 'POST'])
def portfolio():
    form = PortfolioAddForm()
    if form.validate_on_submit():
        try:
            portfolio = Portfolio(name=form.data['name'])
            db.session.add(portfolio)
            db.session.commit()
        except (DBAPIError, IntegrityError) as e:
            flash(str(e.__cause__))
            return redirect(url_for('.portfolio'))

        return redirect(url_for('.search'))

    portfolios = Portfolio.query.all()
    return render_template('portfolio.html', portfolios=portfolios, form=form)
