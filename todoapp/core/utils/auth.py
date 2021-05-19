from flask import current_app 
import uuid


def validate_admin(data):

	uname = data.get('username', None)
	if uname is None or uname != current_app.config.get('ADMIN_USERNAME'):
		return False 

	passwd = data.get('password', None)
	if passwd is None or passwd !=current_app.config.get('ADMIN_PASSWORD'):
		return False 

	return True 


def generate_token():
	return str(uuid.uuid4())