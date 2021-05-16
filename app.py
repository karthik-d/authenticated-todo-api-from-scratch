from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from todoapp.api import blueprint as API

def create_app():
	app = Flask(__name__)
	app.register_blueprint(API, url_prefix=None)
	return app

if __name__ == '__main__':
	app = create_app()
	app.wsgi_app = ProxyFix(app.wsgi_app)
	app.run(debug=True)
