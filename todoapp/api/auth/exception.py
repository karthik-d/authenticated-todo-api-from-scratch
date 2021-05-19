from .namespace import auth_nspace, AUTH_TOKEN_GEN_URL, AUTH_TOKEN_FIELD
from .model import EXCEPTION as exception_model
from .model import AUTH_EXCEPTION as auth_exception_model


class AuthException(Exception):
	"""
	Wrapper exception for all authorization
	related exceptions
	"""

	def __init__(self, http_code, message, *args, **kwargs):
		super(AuthException, self).__init__(*args, **kwargs)
		self.http_code = http_code 
		self.message = message 
		self.token_gen_url = AUTH_TOKEN_GEN_URL
		self.token_field = AUTH_TOKEN_FIELD

	def get_exception(self):
		return {
			key: value for key,value in self.__dict__.items() 
			if key in ['http_code', 'message', 'token_gen_url', 'token_field']
		}


class TokenRequiredException(AuthException):
	"""
	When the request does not have a token  
	and wants to perform an action (read/write) that needs authorization,
	return a custom error message
	"""

	def __init__(self, message="Action require authorization. Supply token", *args, **kwargs):
		http_code = 401
		super(TokenRequiredException, self).__init__(http_code, message, *args, **kwargs)


class ActionForbiddenException(AuthException):
	"""
	When the request does not have a token with 
	require scope to perform an action (read/write),
	return a custom error message
	"""

	def __init__(self, message="Action not allowed. Needs higher scope", *args, **kwargs):
		http_code = 403
		super(ActionForbiddenException, self).__init__(http_code, message, *args, **kwargs)


class InvalidTokenException(AuthException):
	"""
	When the request does not have a valid token with 
	and attempts to perform an action (read/write) that needs one,
	return a custom error message
	"""

	def __init__(self, message="Invalid Token.", *args, **kwargs):
		http_code = 403
		super(InvalidTokenException, self).__init__(http_code, message, *args, **kwargs)


class TokenException(Exception):
	"""
	Wrapper exception for all Token entity 
	related exceptions
	"""

	def __init__(self, http_code, message, *args, **kwargs):
		super(TokenException, self).__init__(*args, **kwargs)
		self.http_code = http_code
		self.message = message 

	def get_exception(self):
		return {
			key: value for key,value in self.__dict__.items() 
			if key in ['http_code', 'message']
		}


class EmptyTokenListException(TokenException):
	"""
	When the token list is empty,
	return a custom error message
	The status is still 'OK' since the request 
	and its handling was successful
	"""

	def __init__(self, message="No tokens in the list", *args, **kwargs):
		http_code = 200
		super(EmptyTokenListException, self).__init__(http_code, message, *args, **kwargs)


class TokenDoesNotExistException(TokenException):
	"""
	When a token of requested id does not exist
	this exception is raised
	"""

	def __init__(self, message="Token could not be found", *args, **kwargs):
		http_code = 404
		super(TokenDoesNotExistException, self).__init__(http_code, message, *args, **kwargs)


class TokenCreationDeniedException(TokenException):
	"""
	When the token will not be create since login credentials failed,
	return a custom error message
	"""

	def __init__(self, message="Could not create new token", *args, **kwargs):
		http_code = 403
		super(TokenCreationDeniedException, self).__init__(http_code, message, *args, **kwargs)


class DidNotCreateTokenException(TokenException):
	"""
	When the token could not be created,
	return a custom error message
	"""

	def __init__(self, message="Could not create new token", *args, **kwargs):
		http_code = 500
		super(DidNotCreateTokenException, self).__init__(http_code, message, *args, **kwargs)



"""
Generic exception handler for AuthException
to dispatch reponse to requests made
to API endpoint when exceptions occur
"""
@auth_nspace.marshal_with(auth_exception_model)
def auth_exception_handler(exception):
	return exception.get_exception(), exception.http_code


"""
Generic exception handler to dispatch reponse to 
requests made to API endpoint when exceptions occur
for the Token entity
"""
@auth_nspace.marshal_with(exception_model)
def token_exception_handler(exception):
	return exception.get_exception(), exception.http_code


