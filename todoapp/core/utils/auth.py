from flask import current_app 


def validate_admin(uname, passwd):
	if uname != current_app.get('ADMIN_USERNAME'):
		return False 
	if passwd !=current_app.get('ADMIN_PASSWORD'):
		return False 
	return True 


def generate_token