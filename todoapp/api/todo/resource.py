"""
Creates  all todo_model related resources
to registers their routes to the todo namespace
"""

from flask_restplus import Resource
from flask import Request

from todoapp.core.dao.todo import Todo as TodoDAO
from .model import todo_nspace, todopatch_parser
from .model import TODO as todo_model
from .model import TODO_WITH_MESSAGE as todo_msg_model

from .exception import (
	EmptyTodoListException, 
	TodoDoesNotExistException,
	DidNotCreateTodoException, 
	DidNotDeleteTodoException
)


@todo_nspace.route(
	'/', 
	methods=[ 'GET', 'POST' ],
	endpoint='todos'
)
class TodoList(Resource):

	@todo_nspace.doc('list_todos')
	@todo_nspace.marshal_list_with(todo_model)
	def get(self):
		"""
		List all the tasks
		"""
		todos = TodoDAO.all()
		if not todos:
			raise EmptyTodoListException
		else:
			return todos, 200

	@todo_nspace.doc('create_todo')
	@todo_nspace.expect(todo_model, validate=True)
	@todo_nspace.marshal_with(todo_msg_model)
	def post(self):
		"""
		Create a new task (status - optional)
		"""

		todo = TodoDAO.create(todo_nspace.payload)
		if todo is None:
			raise DidNotCreateTodoException
		else:
			return {
					"data": todo,
					"message": "Following todos were created"
					}, 201


@todo_nspace.route(
	'/overdue', 
	methods=[ 'GET' ], 
	endpoint='overdue_todos'
)
class OverdueTodoList(Resource):
	"""
	Resource that provides and endpoint to all overdue todos
	An overdue todo is "due before today" AND "unfinished"
	"""

	@todo_nspace.doc('list_todos')
	@todo_nspace.marshal_list_with(todo_msg_model)
	def get(self):
		"""
		List all the overdue tasks (due before today and not finished)
		"""

		todos = TodoDAO.overdue()
		if not todos:
			raise EmptyTodoListException("No tasks are overdue")
		else:
			return {
					"data": todos,
					"message": "Following todos are overdue (not finished and due before today)"
					}, 200


@todo_nspace.route(
	'/due', 
	methods=[ 'GET' ], 
	endpoint='todos_by_due_date'
)
class FinsishedTodoList(Resource):
	"""
	Resource that provides and endpoint to all finished todos
	A finsihed todo has status "Finished"
	"""

	@todo_nspace.doc('list_todos')
	@todo_nspace.marshal_list_with(todo_msg_model)
	def get(self):
		"""
		List all the finished tasks
		"""

		todos = TodoDAO.finished()
		if not todos:
			raise EmptyTodoListException("No tasks are finished")
		else:
			return {
					"data": todos,
					"message": "Following todos are finished"
					}, 200


@todo_nspace.route(
	'/finished', 
	methods=[ 'GET' ], 
	endpoint='finished_todos'
)
class FinsishedTodoList(Resource):
	"""
	Resource that provides and endpoint to all finished todos
	A finsihed todo has status "Finished"
	"""

	@todo_nspace.doc('list_todos')
	@todo_nspace.marshal_list_with(todo_msg_model)
	def get(self):
		"""
		List all the overdue tasks
		"""

		todos = TodoDAO.finished()
		if not todos:
			raise EmptyTodoListException("No tasks are finished")
		else:
			return {
					"data": todos,
					"message": "Following todos are finished"
					}, 200


@todo_nspace.route(
	'/<int:id>', 
	methods=[ 'GET', 'DELETE', 'PUT', 'PATCH' ], 
	endpoint='todo'
)
@todo_nspace.response(404, 'Could not find that todo')
@todo_nspace.param('id', 'The task ID (unique) ')
class Todo(Resource):

	@todo_nspace.doc('get_todo')
	@todo_nspace.marshal_with(todo_model)
	def get(self, id):
		"""
		Display the details of a sepecific task
		"""

		todo = TodoDAO.get(id)
		if todo is None:
			todo_nspace.abort(404, "Todo {} doesn't exist".format(id))
		else:
			return todo

	@todo_nspace.doc('delete_todo')
	@todo_nspace.response(200, 'Following todo was deleted')
	@todo_nspace.marshal_with(todo_msg_model)
	def delete(self, id):
		"""
		Delete a todo by its ID
		"""

		todo = TodoDAO.get(id)
		if todo is None:
			raise TodoDoesNotExistException("Todo {} doesn't exist".format(id))

		id_ = TodoDAO.delete(id)
		if id_ is None:
			raise DidNotDeleteTodoException
		else:
			return {
					"data": todo,
					"message": "Following todo was deleted"
					}, 200

	@todo_nspace.expect(todo_model, validate=True)
	@todo_nspace.response(200, 'Todo was updated to the following')
	@todo_nspace.marshal_with(todo_msg_model)
	def put(self, id):
		"""
		[Entirely] Update a todo entity, by specifying the new state of ALL the fields
		"""

		todo = TodoDAO.update(id, todo_nspace.payload)
		if todo is None:
			raise TodoDoesNotExistException("Todo {} doesn't exits".format(id))
		else:
			return {
					"data": todo,
					"message": "Todo was updated to the following"
					}, 200

	@todo_nspace.response(200, 'Todo was updated to the following')
	@todo_nspace.marshal_with(todo_msg_model)
	def patch(self, id):
		"""
		[Partially] Update a todo entity, by specifying ONLY the fields to be modified
		"""

		payload = todopatch_parser.parse_args()
		todo = TodoDAO.patch_update(id, payload)
		if todo is None:
			raise TodoDoesNotExistException("Todo {} doesn't exits".format(id))
		else:
			return {
					"data": todo,
					"message": "Todo was updated to the following"
					}, 200