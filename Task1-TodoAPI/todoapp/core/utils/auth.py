from flask import current_app 

from todoapp.core.dao.token import Token as TokenDAO


ACCESS_SCOPE = {
	'readonly' : 0,
	'readwrite': 1,
	'admin' : 	2
}


AUTH_NAME = 'OAuth2_Implicit'

AUTH_TOKEN_FIELD = 'X-Api-Key'

AUTH_TOKEN_GEN_URL = '/oauth/authorize'

ACCESS_SCOPE = {
	'readonly' : 0,
	'readwrite': 1,
	'admin' : 	2
}

ACCESS_SCOPE_REV = {
	0 : 'readonly',
	1 : 'readwrite',
	2 : 'admin'
}

AUTH_SPEC = {
	AUTH_NAME: {
		'type' : 'oauth2',
		'description' : 'OAuth2 - Implicit Authentication Scheme with Scopes',
		'flow' : 'implicit',
		'authorizationUrl' : '/oauth/authorize',
		'scopes' : {
			'readonly' : 'Read-only access',
			'readwrite' : 'Read-Write access',
			'admin' : 'Additionaly access to view tokens'
		}
	},
	'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API'
    }
}


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


def validate_scope_name(scope):
	return ACCESS_SCOPE.get(scope, None)	


def get_best_scope(scopes):
	best_scope = -1
	for scope in scopes:
		scope_id = validate_scope_name(scope)
		if scope_id is None:
			continue   # Ignore unknown scopes
		if best_scope < scope_id:
			best_scope = scope_id 
	return best_scope


def validate_client(client_id):
	known_clients = current_app.config.get('CLIENT_IDS')
	return client_id in known_clients
	
