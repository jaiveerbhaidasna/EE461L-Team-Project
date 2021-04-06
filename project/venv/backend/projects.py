from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort
from pymongo import MongoClient
from backend.db import get_login_db, get_project_db

bp = Blueprint('projects', __name__)
@bp.route('/projects', methods=('GET', 'POST'))
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
		flash(error)
	return render_template('projects/projects.html')