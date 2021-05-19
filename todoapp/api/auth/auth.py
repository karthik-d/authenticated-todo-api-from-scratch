"""
Specification of the authorization schemes allowed
"""

from functools import wraps
import types
from flask import request

from todoapp.core.utils.auth import validate_token
from .custom_fields import Scope


AUTH_NAME = 'OAuth2_Implicit'

AUTH_TOKEN_FIELD = 'X-Api-Key'

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


class RequestAuth:

	def __init__(self, *args, **kwargs):
		super(RequestAuth, self).__init__()
		self.token_dict = None
		self.set_token_dict()

	def set_token_dict(self):
		#Memoized
		if self.token_dict is None:
			token_in = request.headers.get(AUTH_TOKEN_FIELD, None)
			if token_in is None:
				print("ERROR")
			token_d = validate_token(token_in)
			if token_d is None:
				print("ERROR")
			self.token_dict = token_d


"""
Decorator function to create a wrapper around
Resource-Classes that checks for
a valid api-token in the request-header
Raises error otherwise if not found
Else, an instance of RequestAuth to the 
Resource-Class
"""
def require_token(ResourceClass):
	base_ctor = ResourceClass.__init__
	def mod_ctor(self, *args, **kwargs):
		base_ctor(self, *args, **kwargs)
		self.request_auth = RequestAuth()
	ResourceClass.__init__ = mod_ctor	
	return ResourceClass

"""
Decorator function to create a wrapper
that checks the wrapped Resource-function's
access requirements against the scope of the 
request token. 
Associated Resource-Class MUST BE decorated by
'@require_token'
"""
def accesslevel(scope, resource_handler):
	@wraps(resource_handler)
	def wrapper(*args, **kwargs):
		pass

