from flask import render_template, flash, redirect, url_for, session, abort, g
from .models import db, User
from .forms import AuthForm
from . import app
import functools


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # abort(404)
            return redirect(url_for('.login'))
        return view(**kwargs)
    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = AuthForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        if not email or not password:
            error = 'Invalid email or password'
        if User.query.filter_by(email=email).first():
            error = f'{ email } has already been registered'

        if not error:
            user = User(
                email=email,
                raw_pass=password
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration complete, please log in again')
            return redirect(url_for('.login'))

        flash(error)

    return render_template('auth/register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # import pdb; pdb.set_trace()
    form = AuthForm()
    if form.validate_on_submit():
        email = form.data['email']
        password = form.data['password']
        error = None

        user = User.query.filter_by(email=email).first()
        if not user or not User.check_password_hash(user, password):
            error = 'Invalid username or password'

        if not error:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('.home'))

        flash(error)

    return render_template('auth/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('OK bye')
    return redirect(url_for('.login'))
