import functools
from .__init__ import app
from flask_cors import CORS, cross_origin
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from backend.db import get_login_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
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

@app.route('/auth/register', methods=('GET', 'POST'))
@cross_origin(supports_credentials=True)
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
        email_found = db.find_one({"email":email})
        if email_found is not None:
        	error = 'email already taken'

        if error is None:
            entry = {
            	"email" : (email),
            	"password" : (password),
            	"projects" : []
            }
            e = db.insert_one(entry).inserted_id        
            
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@app.route('/auth/login', methods=('GET', 'POST'))
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
            return redirect(url_for('projects.projects'))
    	flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))