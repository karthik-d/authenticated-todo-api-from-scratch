import os
from flask import Flask
from werkzeug.contrib.fixers import ProxyFix


def register_blueprints(app):
	from todoapp.authpages import blueprint as Auth 
	app.register_blueprint(Auth, url_prefix='/oauth')
	from todoapp.api import blueprint as API
	app.register_blueprint(API, url_prefix=None)


def register_error_handlers(app):
	from todoapp.api.auth.exception import TokenException, token_exception_handler
	app.register_error_handler(TokenException, token_exception_handler)
	from todoapp.api.todo.exception import TodoException, todo_exception_handler
	app.register_error_handler(TodoException, todo_exception_handler)


def ensure_instance_path(app):
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass


def define_paths(app):
	app.config.update(
		DB_PATH = os.path.join(app.instance_path, app.config['DB_NAME']),
		DB_MIGRATIONS_PATH = os.path.join(	
			app.root_path, 
			'todoapp',
			'core',
			'db',
			'migrations'
		)
	)

def create_app():
	""" 
	Imports and registers all app blueprints
	Initializes Database
	Return the initialised application handle
	"""	
	
	app = Flask(__name__)	
	app.wsgi_app = ProxyFix(app.wsgi_app)
	register_blueprints(app)
	register_error_handlers(app)
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
