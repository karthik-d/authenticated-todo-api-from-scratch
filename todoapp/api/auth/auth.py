"""
Authorization decorators to enforce authorization
on request on demand by resouces
"""

from functools import wraps
import types
from flask import request

from todoapp.core.utils.auth import validate_token
from .custom_fields import Scope
from .namespace import AUTH_TOKEN_FIELD

from .exception import (
	TokenRequiredException, 
	InvalidTokenException
)


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
				raise TokenRequiredException
			token_d = validate_token(token_in)
			if token_d is None:
				raise InvalidTokenException
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

