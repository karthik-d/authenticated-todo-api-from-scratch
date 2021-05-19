from flask_restplus import Namespace


AUTH_NAME = 'OAuth2_Implicit'

AUTH_TOKEN_FIELD = 'X-Api-Key'

AUTH_TOKEN_GEN_URL = '/oauth/authorize'

ACCESS_SCOPE = {
	'readonly' : 0,
	'readwrite': 1,
	'admin' : 	2
}

AUTH_SPEC = {
	AUTH_NAME: {
		'type' : 'oauth2',
		'description' : 'OAuth2 - Implicit Authentication Scheme with Scopes',
		'flow' : 'implicit',
		'authorizationUrl' : '/oauth/authorize',
		'scopes' : {
			'read' : 'Read-only access',
			'write' : 'Read-Write access'
		}
	}
}

# Create the namespace
auth_nspace = Namespace(
	'auth', 
	description='Authorization for API operations'
)