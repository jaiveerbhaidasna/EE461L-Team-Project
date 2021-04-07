from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import functools
from flask_cors import CORS, cross_origin
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
#from . import get_login_db

client = MongoClient(
    "mongodb+srv://ADMIN:GROUP15@cluster.jeu90.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

app = Flask(__name__)


def create_app():
    cors = CORS(app, support_credentials=True)
    app.config.from_mapping(SECRET_KEY='dev')

    @app.route('/home')
    def home():
        return "Home Page"

    from . import db
    # db.init_app(app)

    from . import auth, projects
    app.register_blueprint(auth.bp)
    app.register_blueprint(projects.bp)

    return app


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db = get_login_db()
        error = None
        if not email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'
        email_found = db.find_one({"email": email})
        if email_found is not None:
            error = 'email already taken'

        if error is None:
            entry = {
                "email": (email),
                "password": (password),
                "projects": []
            }
            e = db.insert_one(entry).inserted_id

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')
