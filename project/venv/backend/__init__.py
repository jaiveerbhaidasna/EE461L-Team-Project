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
from bson.objectid import ObjectId

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
            return redirect(url_for('get_projects'))
    return("This is being returned in place of a login HTML")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

"""@app.route('/', methods=('GET','POST'))
def load_project():
    if(request.method == 'POST'):
        dictionary = json.loads(json.dumps(request.json))
        project_id = dictionary['id']
        db = get_project_db
        error = None
        project_found = db.find_one({"id":project_id})
        if project_found is not None:
            # Load project
            session['project id'] = project_id
            #return redirect(url_for('check_in'))
    return "Failed to load project"
"""

@app.route('/projects', methods=('GET', 'POST'))
def projects():
    # Give the user the option to create a new project

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
            #return redirect(url_for('workspace'))
            
    return "Failed to create a new project"

@app.route('/project/checkin', methods=('GET','POST'))
def check_in():
    # Given the name of the hardware set, and the amount requested to check in
    if (request.method == 'POST'):
        # Parse the input
        dictionary = json.loads(json.dumps(request.json))
        name = dictionary['name']
        amount = dictionary['request']

        # Get the current project id from session
        project_id = session['project id']

        # Search for the project in the database
        project_db = get_project_db()
        project_data = project_db.find_one({"id":project_id})

        # Try to get the project's corresponding hardware sets
        hardware_db = get_hardware_set_db()
        hardware_object_id = None
        # Get the wanted hardware set's MongoDB Object ID
        hardware_array = project_data['hardware sets']
        if name == "Hardware Set 1":
            hardware_object_id = hardware_array[0]
        elif name == "Hardware Set 2":
            hardware_object_id = hardware_array[1]

        error = None

        # Try to find the hardware set in the database
        hardware_set = hardware_db.find_one({"_id":hardware_object_id})
        if (hardware_set is None):
            error = 'No matching Hardware Set with given ID'

        current_available = hardware_set['available']
        #name_found_capacity = name_found['capacity']
        
        if (error is None):
            db.update_one({"_id":_id}, {"$set": { 'available':  current_available + int(amount)}})
            return 'Success'

    return error

@app.route('/project/checkout', methods=('GET','POST'))
def check_out():
    # Given the name of the hardware set, and the amount requested to check out
    if (request.method == 'POST'):
        # Parse the input
        dictionary = json.loads(json.dumps(request.json))
        name = dictionary['name']
        amount = dictionary['request']

        # Get the current project id from session
        project_id = session['project id']

        # Search for the project in the database
        project_db = get_project_db()
        project_data = project_db.find_one({"id":project_id})

        # Try to get the project's corresponding hardware sets
        hardware_db = get_hardware_set_db()
        hardware_object_id = None
        # Get the wanted hardware set's MongoDB Object ID
        hardware_array = project_data['hardware sets']
        if name == "Hardware Set 1":
            hardware_object_id = hardware_array[0]
        elif name == "Hardware Set 2":
            hardware_object_id = hardware_array[1]

        error = None

        # Try to find the hardware set in the database
        hardware_set = hardware_db.find_one({"_id":hardware_object_id})
        if (hardware_set is None):
            error = 'No matching Hardware Set with given ID'

        current_available = hardware_set['available']
        #name_found_capacity = name_found['capacity']
        
        if (error is None):
            db.update_one({"_id":_id}, {"$set": { 'available':  current_available - int(amount)}})
            return 'Success'

    return error

@app.route('/', methods=('GET','POST'))    
def get_projects():
    if (request.method == 'GET'):
        # Case 1 
        db = get_project_db()
        error = None
        projects = str(list(db.find({})))
        output = []
        for p in projects:
            all_projects = str(list(p))
            h_index = all_projects.index('\'hardware sets')
            lastitem = all_projects[h_index:-1]
            all_projects = all_projects[:h_index]
            splitlist = all_projects.split(', ')
            splitlist.pop(0)
            splitlist.pop()
            #print(lastitem)
            #print(splitlist)
            project_dict = {}
            for i in range(0,len(splitlist)):
                element = splitlist[i]
                colon_index = element.index(':')
                print(element.index(':'))
                project_dict[element[:colon_index]] = element[colon_index + 1:]
            colon_index = lastitem.index(':')
            project_dict[lastitem[:colon_index]] = lastitem[colon_index + 1:]
            output.append(json.dumps(project_dict))
            #print(json.dumps(output))
        
        return output

    return 'Failed to get projects'

@app.route('/<id>', methods=('GET','POST'))
def get_single_project(id):
    if(request.method == 'GET'):
        project_db = get_project_db()
        hardware_db = get_hardware_set_db()
        output = []             
        project_data = project_db.find_one({"id":int(id)})
        hardware_set_array = project_data['hardware sets']
        hardware_id_1 = hardware_set_array[0]  
        hardware_id_2 = hardware_set_array[1] 
        print(hardware_set_array[0])  
        hardware_set_1_data = str(list(hardware_db.find({"_id":hardware_id_1})))        
        hardware_set_2_data = str(list(hardware_db.find({"_id":hardware_id_2})))

        name_index1 = hardware_set_1_data.index('\'name')
        name_index2 = hardware_set_2_data.index('\'name')
        hardware_set_1_data = hardware_set_1_data[name_index1:]
        hardware_set_2_data = hardware_set_2_data[name_index2:]
        

        h1_data = '\"{'
        quote_count = 0
        for ch in hardware_set_1_data:
            if ch != '\'' or quote_count == 2 or quote_count == 3:
                h1_data+= ch
            if ch == '\'':
                quote_count+=1

        h2_data = '\"{'
        quote_count = 0
        for ch in hardware_set_2_data:
            if ch != '\'' or quote_count == 2 or quote_count == 3:
                h2_data+= ch
            if ch == '\'':
                quote_count+=1

        h1_data = h1_data[:-1] + '\"'
        h2_data = h2_data[:-1] + '\"'


        output.append(h1_data)
        output.append(h2_data)
        print(str(output))


        return json.dumps(output)


                   




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