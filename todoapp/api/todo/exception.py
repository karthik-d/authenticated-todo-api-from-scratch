#from flask_restplus import marshal

from .model import todo_nspace
from .model import EXCEPTION as exception_model
from .model import EXCEPTION_WITH_DATA as exception_data_model


class TodoException(Exception):
	"""
	Wrapper exception for all Todo entity 
	related exceptions
	"""

	def __init__(self, message, todo=None):
		Exception.__init__(self)
		self.message = message 
		self.data = todo

	def has_data(self):
		if self.data is None:
			return False 
		else:
			return True


class EmptyTodoListException(TodoException):
	"""
	When the todo list is empty,
	return a custom error message
	The status is still 'OK' since the request 
	and its handling was successful
	"""

	def __init__(self, message="No todos in the list"):
		TodoException.__init__(self, message, None)
		self.http_code = 200


class DidNotCreateTodoException(TodoException):
	"""
	When the todo could not be created,
	return a custom error message
	"""

	def __init__(self, message="Could not create new todo", todo=None):
		TodoException.__init__(self, message, todo)
		self.http_code = 500


class DidNotDeleteTodoException(TodoException):
	"""
	When the todo could not be created,
	return a custom error message
	"""

	def __init__(self, message="Could not create new todo", todo=None):
		TodoException.__init__(self, message)
		self.http_code = 500


def todo_exception_handler(exception):
	if(exception.has_data()):
		return todo_nspace.marshal(
					exception.__dict__, 
					exception_data_model
				), exception.http_code
	else:
		return todo_nspace.marshal(
					exception.__dict__, 
					exception_model
				), exception.http_code


