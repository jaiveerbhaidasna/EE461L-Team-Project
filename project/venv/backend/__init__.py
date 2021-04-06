from flask import Flask
from pymongo import MongoClient

client = MongoClient("mongodb+srv://ADMIN:GROUP15@cluster.jeu90.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

def create_app():
	app = Flask(__name__)
	app.config.from_mapping(SECRET_KEY='dev')
	@app.route('/home')
	def home():
		return "Home Page"

	from . import db
	#db.init_app(app)

	from . import auth, projects
	app.register_blueprint(auth.bp)
	app.register_blueprint(projects.bp)

	return app	