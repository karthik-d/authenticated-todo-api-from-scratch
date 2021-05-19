from flask import current_app 

from todoapp.core.dao.token import Token as TokenDAO


def validate_admin(data):
	uname = data.get('username', None)
	if uname is None or uname != current_app.config.get('ADMIN_USERNAME'):
		return False 

	passwd = data.get('password', None)
	if passwd is None or passwd !=current_app.config.get('ADMIN_PASSWORD'):
		return False 

	return True


def validate_token(token):
	token_row = TokenDAO.get(token)
	if token_row is None:
		return None
	else:
		return dict(token_row)
