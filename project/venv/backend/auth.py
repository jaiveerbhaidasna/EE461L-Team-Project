import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from backend.db import get_db

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

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        username_found = db.find_one({"username":username})
        if username_found is not None:
        	error = 'Username already taken'

        if error is None:
            entry = {
            	"username" : encrypt(username),
            	"password" : encrypt(password)
            }
            e = db.insert_one(entry).inserted_id        
            
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        username_found = db.find_one({"username":username})
        password_found = db.fine_one({"password":password})
        if username_found is None or password_found is none:
            error = 'No matching username and password combination'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    #else: (get user project data)
        #g.user = get_db.find_one({"username":user_id})

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view