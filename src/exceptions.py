from . import app
from flask import render_template


@app.errorhandler(404)
def not_found(error):
    """ Custom 404 handler """
    return render_template('exceptions/404.html', error=error), 404


@app.errorhandler(400)
def bad_request(error):
    """ Custom 400 handler """
    return render_template('exceptions/400.html', error=error), 400
