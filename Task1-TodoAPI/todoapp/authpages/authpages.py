""" 
Creates the Auth Pages blueprint for this package
Registered to the app
"""

from flask import Blueprint

blueprint = Blueprint(
	'authpages',
	 __name__, 
	 template_folder='./templates'
	)