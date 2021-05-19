from .namespace import auth_nspace
from .model import EXCEPTION as exception_model


class AuthException(Exception):
	"""
	Wrapper exception for all authorization
	related exceptions
	"""

	def __init__(self, http_code, message, *args, **kwargs):
		super(AuthException, self).__init__(*args, **kwargs)
		self.http_code = http_code 
		self.message = message 

	def get_exception(self):
		return {
			key: value for key,value in self.__dict__.items() 
			if key in ['http_code', 'message']
		}


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
		http_code = 401
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
Generic exception handler to dispatch reponse to 
requests made to API endpoint when exceptions occur
"""
@auth_nspace.marshal_with(exception_model)
def token_exception_handler(exception):
	return exception.get_exception(), exception.http_code


