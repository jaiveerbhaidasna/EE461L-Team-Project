import functools
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

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_login_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        username_found = db.find_one({"username":encrypt(username)})
        if username_found is not None:
        	error = 'Username already taken'

        if error is None:
            entry = {
            	"username" : encrypt(username),
            	"password" : encrypt(password),
            	"projects" : []
            }
            e = db.insert_one(entry).inserted_id        
            
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if (request.method == 'POST'):
    	username = request.form['username']
    	password = request.form['password']
    	db = get_login_db()
    	error = None
    	encrypted_username = encrypt(username)
    	username_found = db.find_one({"username":encrypted_username})
    	password_found = db.find_one({"password":encrypt(password)})
    	if (username_found is None or password_found is None):
    		error = 'No matching username and password combination'
    	if (error is None):
            session['username'] = encrypted_username
            return redirect(url_for('projects.projects'))
    	flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))