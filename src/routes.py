from flask import render_template, abort, redirect, url_for, request
#from sqlalchemy.exc import DBAPIError, IntegrityError
from . import app
import requests
import json
import os


@app.route('/')
def home():
    return render_template('home.html')
