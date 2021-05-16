import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix


def ensure_instance_path(app):
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass


def define_paths(app):
	app.config.update(
		DB_PATH = os.path.join(app.instance_path, app.config['DB_NAME']),
		DB_SCRIPTS_PATH = os.path.join(	app.root_path, 
										'todoapp',
										'core',
										'db',
										'scripts'
										)
	)

def create_app():
	""" 
	Imports and registers all app blueprints
	Initializes Database
	Return the initialised application handle
	"""	
	app = Flask(__name__)
	# Register blueprints
	from todoapp.api import blueprint as API
	app.register_blueprint(API, url_prefix=None)	
	app.wsgi_app = ProxyFix(app.wsgi_app)
	# Load configurations
	app.config.from_object('config.ApplicationConfig')
	ensure_instance_path(app)
	define_paths(app)
	# Initialize Database
	from todoapp.core.db import init_db_context 
	init_db_context(app)
	# Return application handle
	return app


if __name__ == '__main__':
	app = create_app()
	app.run(debug=app.config['DEBUG'])


"""
To Run:
 - python app.py
 - export FLASK_APP=app.py && flask run
"""
