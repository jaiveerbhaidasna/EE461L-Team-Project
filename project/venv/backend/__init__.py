from flask import Flask
from pymongo import MongoClient

def create_app():
	app = Flask(__name__)
	#client = MongoClient("mongodb+srv://ADMIN:GROUP15@cluster.jeu90.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
	#db = client.db
	#collection = db['login_info']

	@app.route('/home')
	def home():
		return "Home Page"

	from . import db
	#db.init_app(app)

	from . import auth
	app.register_blueprint(auth.bp)

	return app	