from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import functools
from flask_cors import CORS, cross_origin
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

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

    #from . import auth, projects

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
        #flash(error)
    return "hi"

@app.route('/login', methods=('GET', 'POST'))
def login():
    if (request.method == 'POST'):
        email = request.form.get('email')
        password = request.form.get('password')
        db = get_login_db()
        error = None
        #encrypted_username = encrypt(username)
        email_found = db.find_one({"email":email})
        password_found = db.find_one({"password":password})
        if (email_found is None or password_found is None):
            error = 'No matching email and password combination'
        if (error is None):
            session['email'] = email
            return redirect(url_for('projects'))
        #flash(error)
    #return render_template('auth/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@app.route('/projects', methods=('GET', 'POST'))
def projects():
    # Give the user the option to create a new project or enter the
    # project ID of an existing project
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_id = request.form['new_id']

        existing_id = request.form['existing_id']

        login_db = get_login_db()
        project_db = get_project_db()
        error = None

        if not name and not description and not new_id and not existing_id:
            # Nothing filled out
            error = 'Create a new project or load an existing one'
        elif not existing_id:
            # New project
            if not name or not description or not new_id:
                # Missing at least one input
                error = 'Please fill out the missing fields'
            else:
                # Check if project ID already taken
                new_id_found = project_db.find_one({"project id":new_id})
                if new_id_found is not None:
                    # ID already taken
                    error = 'Project ID already taken'
        else:
            # Load existing project
            if not name or not description or not new_id:
                # Other fields not empty
                error = 'Please delete all unnecessary fields'
            else:
                # Check if project ID exists
                existing_id_found = project_db.find_one({"project id":existing_id})
                if existing_id_found is None:
                    # Project not found
                    error = 'No matching project found'

        if error is None:
            #if existing_id is None:
                # Create new project and add to database
                l = login_db.update_one(
                    {"username":session.get('username')},
                    {'$push': {"projects":new_id}}
                )
                project_info = {
                    "project id":new_id,
                    "name":"Hardware Set 1",
                    "capacity":100,
                    "available":100,
                    "name":"Hardware Set 2",
                    "capacity":100,
                    "available":100
                }
                project_db.insert_one(project_info)
            #else:
                # Load existing project from database
        #flash(error)
    #return render_template('projects/projects.html')


def get_login_db():
    if 'db' not in g:
        g.db = client.db
        g.collection = g.db['login_info']

    return g.collection

def get_project_db():
    if 'db' not in g:
        g.db = client.db
        g.collection = g.db['projects']

    return g.collection
