from .model import todo_nspace
from .model import exception as exception_model


class TodoException(Exception):
	"""
	Wrapper exception for all Todo entity 
	related exceptions
	"""

	def __init__(self):
		Exception.__init__(self)


class EmptyTodoListException(TodoException):
	"""
	When the todo list is empty,
	return a custom error message
	The status is still 'OK' since the request 
	and its handling was successful
	"""

	def __init__(self, message="No todos in the list"):
		TodoException.__init__(self)
		self.http_code = 200
		self.message = message


class DidNotCreateTodoException(TodoException):
	"""
	When the todo could not be created,
	return a custom error message
	"""

	def __init__(self, message="Could not create new todo", ):
		TodoException.__init__(self)
		self.http_code = 500
		self.message = message


@todo_nspace.marshal_with(exception_model)
def todo_exception_handler(exception):
	return exception.__dict__, exception.http_code


