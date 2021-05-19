"""
Specification of the authorization schemes allowed
"""

AUTH_NAME = 'OAuth2_Implicit'

AUTH_SPEC = {
	AUTH_NAME: {
		'type' : 'oauth2',
		'description' : 'OAuth2 - Implicit Authentication Scheme with Scopes',
		'flow' : 'implicit',
		'authorizationUrl' : '/oauth/authorize',
		'scopes' : {
			'read' : 'Read-only access',
			'read-write' : 'Read-Write access',
			'admin' : 'Admin access'
		}
	}
}

"""
AUTH_NAME = 'apikey'
AUTH_SPEC = {
	'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}
"""
