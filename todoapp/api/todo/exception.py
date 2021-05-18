from flask import current_app

from .model import todo_nspace
from .model import exception as exception_model


class EmptyTodoListException(Exception):
	"""
	When the todo list is empty,
	return a custom error message
	The status is still 'OK' since the request 
	and its handling was successful
	"""

	def __init__(self, message="No todos in the list"):
		Exception.__init__(self)
		self.http_code = 200
		self.message = message


@todo_nspace.marshal_with(exception_model)
def empty_todolist_handler(exception):
	return exception.__dict__, exception.http_code