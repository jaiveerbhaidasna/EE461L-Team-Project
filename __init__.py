from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
import functools
from flask_cors import CORS, cross_origin
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import json

client = MongoClient(
    "mongodb+srv://ADMIN:GROUP15@cluster.jeu90.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

app = Flask(__name__)


def create_app():
    cors = CORS(app, support_credentials=True)
    app.config.from_mapping(SECRET_KEY='dev')

    from . import db

    return app

def encrypt(inputText):
    N = 20
    reversed = inputText[::-1]
    reversedList = list(reversed)
    newList = []
    for element in reversedList:
        newAscii = 0
        newAscii = ord(element) + N
        if newAscii > 126:
            newAscii = newAscii - 93
        if newAscii < 34:
            newAscii = newAscii + 93
        newList.append(chr(newAscii))
    return "".join(newList)

def decrypt(inputText):
    N = 20
    reversed = inputText[::-1]
    reversedList = list(reversed)
    newList = []
    for element in reversedList:
        newAscii = 0
        newAscii = ord(element) - N
        if newAscii > 126:
            newAscii = newAscii - 93
        if newAscii < 34:
            newAscii = newAscii + 93
        newList.append(chr(newAscii))
    return "".join(newList)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        dictionary = json.loads(json.dumps(request.json))
        email = dictionary['email']
        password = dictionary['password']
        db = get_login_db()
        error = None
        encrypted_email = encrypt(email)
        encrypted_password = encrypt(password)
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        email_found = db.find_one({"email": encrypted_email})
        if email_found is not None:
            error = 'Email already taken'
      
        if error is None:
            entry = {
                "email": (encrypted_email),
                "password": (encrypted_password),
                "projects": []
            }
            db.insert_one(entry)

            return redirect(url_for('login'))
        
    return "This is being returned in place of a register HTML"

@app.route('/login', methods=('GET', 'POST'))
def login():
    if (request.method == 'POST'):
        dictionary = json.loads(json.dumps(request.json))
        email = dictionary['email']
        password = dictionary['password']
        db = get_login_db()
        error = None
        encrypted_email = encrypt(email)
        encrypted_password = encrypt(password)
        email_found = db.find_one({"email":encrypted_email})
        password_found = db.find_one({"password":encrypted_password})
        if (email_found is None or password_found is None):
            error = 'No matching email and password combination'
        if (error is None):
            session['email'] = encrypted_email
            return redirect(url_for('projects'))
    return("This is being returned in place of a login HTML")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def get_login_db():
    g.db = client.db
    g.collection = g.db['login_info']

    return g.collection

def get_project_db():
    g.db = client.db
    g.collection = g.db['projects']

    return g.collection
