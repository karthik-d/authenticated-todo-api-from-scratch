from flask import current_app 
import uuid


def validate_admin(uname, passwd):
	if uname != current_app.get('ADMIN_USERNAME'):
		return False 
	if passwd !=current_app.get('ADMIN_PASSWORD'):
		return False 
	return True 


def generate_token():
	return str(uuid.uuid4())