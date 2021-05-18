"""
Creates  all todo_model related resources
to registers their routes to the todo namespace
"""

from flask_restplus import Resource
from flask import Request

from todoapp.core.dao.todo import Todo as TodoDAO
from .model import todo_nspace
from .model import todo as todo_model
from .exception import EmptyTodoListException, DidNotCreateTodoException


@todo_nspace.route('/')
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
	@todo_nspace.marshal_with(todo_model, code=201)
	def post(self):
		'''Create a new task'''
		todo = TodoDAO.create(todo_nspace.payload)
		if todo is None:
			raise DidNotCreateTodoException
		else:
			return todo, 201


@todo_nspace.route('/<int:id>')
@todo_nspace.response(404, 'Could not find that todo')
@todo_nspace.param('id', 'The task ID (unique) ')
class Todo(Resource):

	@todo_nspace.doc('get_todo')
	@todo_nspace.marshal_with(todo_model)
	def get(self, id):
		todo = TodoDAO.get(id)
		if todo is None:
			todo_nspace.abort(404, "Todo {} doesn't exist".format(id))
		else:
			return todo

	@todo_nspace.doc('delete_todo')
	@todo_nspace.response(204, 'todo_model deleted')
	def delete(self, id):
		TodoDAO.delete(id)
		return '', 204

	@todo_nspace.expect(todo_model)
	@todo_nspace.marshal_with(todo_model)
	def put(self, id):
		return TodoDAO.update(id, api.payload)