from flask import Flask
from flask_cors import CORS
from flask import jsonify
from flask import request
from pymongo import MongoClient
import functools
from flask_cors import CORS, cross_origin
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import json
import bson
from bson.json_util import dumps
from bson.json_util import loads

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

@app.route('/projects', methods=('GET', 'POST'))
def projects():
    # Give the user the option to create a new project or enter the
    # project ID of an existing project

    # 100 hardware set 1 capacity/available
    # 100 hardware set 2

    if request.method == 'POST':
        dictionary = json.loads(json.dumps(request.json))
        hardware_set_db = get_hardware_set_db()
        name = dictionary['name']
        description = dictionary['description'] 
        id = dictionary['id']
        hardware_set_1_info = {
            "name":"Hardware Set 1",
            "capacity":100,
            "available":100
        }
        hardware_set_2_info = {
            "name":"Hardware Set 2",
            "capacity":100,
            "available":100
        }
        hardware_set_1_id = hardware_set_db.insert_one(hardware_set_1_info).inserted_id
        hardware_set_2_id = hardware_set_db.insert_one(hardware_set_2_info).inserted_id

        hardware_sets = [hardware_set_1_id, hardware_set_2_id]


        login_db = get_login_db()
        project_db = get_project_db()
        error = None

        if not name:
            error = 'name is required'
        if not description:
            error = 'description is required'
        if not id:
            error = 'id is required'
        id_input = project_db.find_one({"id": id})
        if id_input is not None:
            error = 'id is already taken'
        if error is None:
            #if existing_id is None:
                # Create new project and add to database
            project_info = {
                "id":id,
                "name":name,
                "description": description,
                "hardware sets":hardware_sets
            }
            project_db.insert_one(project_info)
            #else:
                # Load existing project from database
        #flash(error)
    return "hi"

@app.route('/hardwaresets/checkin', methods=('GET','POST'))
def check_in():
    if (request.method == 'POST'):
        dictionary = json.loads(json.dumps(request.json))
        _id = dictionary['id']
        amount = dictionary['request']
        db = get_hardware_db()
        error = None

        name_found = db.find_one({"_id":_id})
        if (name_found is None):
            error = 'No matching Hardware Set with given name'

        name_found_available = name_found['available']
        #name_found_capacity = name_found['capacity']
        
        if (error is None and name_found_available):
            db.update_one({"_id":_id}, {"$set": { 'available':  name_found_available + int(amount)}})
            return 'Success'

    return 'Failure'

@app.route('/hardwaresets/checkout', methods=('GET','POST'))
def check_out():
    if (request.method == 'POST'):
        dictionary = json.loads(json.dumps(request.json))
        _id = dictionary['id']
        amount = dictionary['request']
        db = get_hardware_db()
        error = None

        name_found = db.find_one({"_id":_id})
        if (name_found is None):
            error = 'No matching Hardware Set with given name'

        name_found_available = name_found['available']
        
        if (error is None and name_found_available >= int(amount)):
            db.update_one({"_id":_id}, {"$set": { 'available':  name_found_available - int(amount)}})
            return 'Success'

    return 'Failure'

@app.route('/', methods=('GET','POST'))    
def get_projects():
    if (request.method == 'GET'):
        # Case 1 
        db = get_project_db()
        error = None
        all_projects = str(list(db.find({}))[0])
        splitlist = all_projects.split(',')
        splitlist.pop(0)
        splitlist[0] = "{" + splitlist[0]
        
        #print(all_projects)
        #projects = jsonify(all_projects)
        # Might need to convert to JSON
        return "test"

    return 'Failure'

@app.route('/<id>', methods=('GET','POST'))
def get_single_project(id):
    if(request.method == 'GET'):
        print(id)
        #id = request.path
        db = get_project_db()
        project = list(db.find({"id":id}))
        jsonproject = str(project)
        print(project)
        print(jsonproject)
        return jsonproject
    return "Failure"



def get_login_db():
    g.db = client.db
    g.collection = g.db['login_info']

    return g.collection

def get_project_db():
    g.db = client.db
    g.collection = g.db['projects']

    return g.collection

def get_hardware_set_db():
    g.db = client.db
    g.collection = g.db['hardware sets']

    return g.collection
