import click
from flask import current_app, g
from pymongo import MongoClient
from backend.__init__ import client

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

"""
def close_db():
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
"""