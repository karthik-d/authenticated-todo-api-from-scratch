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
			'write' : 'Read-Write access'
		}
	}
}

