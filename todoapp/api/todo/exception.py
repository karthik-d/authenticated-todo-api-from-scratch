#from flask_restplus import marshal

from .namespace import todo_nspace
from .model import EXCEPTION as exception_model
from .model import EXCEPTION_WITH_DATA as exception_data_model


class TodoException(Exception):
	"""
	Wrapper exception for all Todo entity 
	related exceptions
	"""

	def __init__(self, message, todos=None):
		super(TodoException, self).__init__()
		self.message = message 
		self.data = todos

	def has_data(self):
		if self.data is None:
			return False 
		else:
			return True

	def get_exception(self):
		return {
			key: value for key,value in self.__dict__.items() 
			if key in ['http_code', 'message']
		}

	def get_data(self):
		return self.data


class EmptyTodoListException(TodoException):
	"""
	When the todo list is empty,
	return a custom error message
	The status is still 'OK' since the request 
	and its handling was successful
	"""

	def __init__(self, message="No todos in the list"):
		super(TodoException, self).__init__(message, None)
		self.http_code = 200


class TodoDoesNotExistException(TodoException):
	"""
	When a todo of requested id does not exist
	this exception is raised
	"""

	def __init__(self, message="Todo could not be found"):
		super(TodoException, self).__init__(message, None)
		self.http_code = 404


class DidNotCreateTodoException(TodoException):
	"""
	When the todo could not be created,
	return a custom error message
	"""

	def __init__(self, message="Could not create new todo", todos=None):
		super(TodoException, self).__init__(message, todos)
		self.http_code = 500


class DidNotDeleteTodoException(TodoException):
	"""
	When the todo could not be created,
	return a custom error message
	"""

	def __init__(self, message="Could not delete todo", todos=None):
		super(TodoException, self).__init__(message, todos)
		self.http_code = 500


"""
Generic exception handler to dispatch reponse to 
requestrs made to API endpoint when excpetions occur
"""
def todo_exception_handler(exception):
	if(exception.has_data()):
		return todo_nspace.marshal(
			{
			'exception': exception.get_exception(),
			'data': exception.get_data()
			}, 
			exception_data_model
		), exception.http_code
	else:
		return todo_nspace.marshal(
			exception.get_exception(), 
			exception_model
		), exception.http_code


