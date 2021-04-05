import click
from flask import current_app, g
from pymongo import MongoClient

def get_db():
	if 'db' not in g:
		g.client = MongoClient("mongodb+srv://ADMIN:GROUP15@cluster.jeu90.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
		g.db = g.client.db
		g.collection = g.db['login_info']

	return g.collection

"""
def close_db():
	db = g.pop('db', None)

	if db is not None:
		db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
"""