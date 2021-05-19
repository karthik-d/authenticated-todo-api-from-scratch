"""
Creates  all todo_model related resources
to registers their routes to the todo namespace
"""

from flask_restplus import Resource
from datetime import date

from todoapp.api.auth import (
	AUTH_NAME, 
	ACCESS_SCOPE, 
	require_token,
	require_accesslevel
)

from todoapp.core.dao.todo import Todo as TodoDAO
from .namespace import todo_nspace
from .model import TODO as todo_model
from .model import TODO_WITH_MESSAGE as todo_msg_model
from .request_parser import TodoPatch_Parser, DateArg_Parser
from .custom_fields import Status

from .exception import (
	EmptyTodoListException, 
	TodoDoesNotExistException,
	DidNotCreateTodoException, 
	DidNotDeleteTodoException
)

@require_token
@todo_nspace.route(
	'/', 
	methods=[ 'GET', 'POST' ],
	endpoint='todos'
)
class TodoList(Resource):

	def __init__(self, *args, **kwargs):
		super(TodoList, self).__init__(*args, **kwargs)

	
	@require_accesslevel(ACCESS_SCOPE.get('readonly'))
	@todo_nspace.doc('list_todos', security=[{AUTH_NAME: ['read', 'write']}])
	@todo_nspace.response(200, "{ list of all tasks } ( OR ) No tasks in the todo-list")
	@todo_nspace.marshal_list_with(todo_model)
	def get(self):
		"""
		List all the tasks
		"""
		
		todos = TodoDAO.all()
		if not todos:
			raise EmptyTodoListException("No tasks in the todo-list")
		else:
			return todos, 200


	@require_accesslevel(ACCESS_SCOPE.get('readwrite'))
	@todo_nspace.doc('create_todo')
	@todo_nspace.response(201, "Following tasks were added to the todo list + { created tasks' details }")
	@todo_nspace.response(500, "Could not create task")
	@todo_nspace.expect(todo_model, validate=True)
	@todo_nspace.marshal_with(todo_msg_model)
	def post(self):
		"""
		Create a new task (status - optional)
		"""
		
		if todo_nspace.payload.get('status', None) is None:
			todo_nspace.payload['status'] = Status().default
		todo = TodoDAO.create(todo_nspace.payload)
		if todo is None:
			raise DidNotCreateTodoException("Could not create task")
		else:
			return {
					"data": todo,
					"message": "Following tasks were added to the todo list"
					}, 201


@require_token
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

	@require_accesslevel(ACCESS_SCOPE.get('readonly'))
	@todo_nspace.doc('list_todos')
	@todo_nspace.response(200, "Following tasks are overdue + { overdue tasks } ( OR ) No tasks are overdue")
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
					"message": "Following tasks are overdue (not finished and due before today)"
					}, 200


@require_token
@todo_nspace.route(
	'/due', 
	methods=[ 'GET' ], 
	endpoint='todos_by_due_date'
)
class TodoListByDueDate(Resource):
	"""
	Resource that provides and endpoint to todos due on a specific day
	This determined by the due_date argument passed in the URL
	If no date is passed, current date is used
	"""

	@require_accesslevel(ACCESS_SCOPE.get('readonly'))
	@todo_nspace.doc('list_todos')
	@todo_nspace.response(200, "Following 'unfinished' tasks are due on {date} + { due tasks }")
	@todo_nspace.marshal_list_with(todo_msg_model)
	def get(self):
		"""
		List all the "Unfinished" tasks due on 'due_date' in args if specified, else current date
		"""

		payload = DateArg_Parser.parse_args()
		due_date = payload.get('due_date', date.today())
		due_date_str = due_date.strftime('%Y-%m-%d')
		todos = TodoDAO.due_on(due_date)
		if not todos:
			raise EmptyTodoListException("No tasks are due on {date}".format(date=due_date_str))
		else:
			return {
					"data": todos,
					"message": "Following 'unfinished' tasks are due on {date}".format(date=due_date_str)
					}, 200


@require_token
@todo_nspace.route(
	'/finished', 
	methods=[ 'GET' ], 
	endpoint='finished_todos'
)
class FinsishedTodoList(Resource):
	"""
	Resource that provides an endpoint to all finished todos
	A finsihed todo has status "Finished"
	"""

	@require_accesslevel(ACCESS_SCOPE.get('readonly'))
	@todo_nspace.doc('list_todos')
	@todo_nspace.response(200, "Following tasks are finished + { finished tasks } ( OR ) No tasks are finished")
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
					"message": "Following tasks are finished"
					}, 200


@require_token
@todo_nspace.route(
	'/<int:id>', 
	methods=[ 'GET', 'DELETE', 'PUT', 'PATCH' ], 
	endpoint='todo'
)
@todo_nspace.param('id', 'The task ID (unique) ')
class Todo(Resource):
	"""
	Resource that provides an endpoint to a single todo instance
	Specified by the id parameter in the URL
	"""

	@require_accesslevel(ACCESS_SCOPE.get('readonly'))
	@todo_nspace.doc('get_todo')
	@todo_nspace.response(200, "{ requested task }")
	@todo_nspace.response(404, "Task with ID {id} doesn't exist")
	@todo_nspace.marshal_with(todo_model)
	def get(self, id):
		"""
		Display the details of a sepecific task
		"""

		todo = TodoDAO.get(id)
		if todo is None:
			raise TodoDoesNotExistException("Task with ID {id_} doesn't exist".format(id_=id))
		else:
			return todo

	
	@require_accesslevel(ACCESS_SCOPE.get('readwrite'))
	@todo_nspace.doc('delete_todo')
	@todo_nspace.response(200, "Following task was deleted + { deleted task details }")
	@todo_nspace.response(404, "Task with ID {id} doesn't exist")
	@todo_nspace.marshal_with(todo_msg_model)
	def delete(self, id):
		"""
		Delete a todo by its ID
		"""

		todo = TodoDAO.get(id)
		if todo is None:
			raise TodoDoesNotExistException("Task with ID {id_} doesn't exist".format(id_=id))

		id_ = TodoDAO.delete(id)
		if id_ is None:
			raise DidNotDeleteTodoException
		else:
			return {
					"data": todo,
					"message": "Following task was deleted"
					}, 200

	
	@require_accesslevel(ACCESS_SCOPE.get('readwrite'))
	@todo_nspace.expect(todo_model, validate=True)
	@todo_nspace.response(200, "Task was updated as follows + { udpated task details }")
	@todo_nspace.response(404, "Task with ID {id} doesn't exist")
	@todo_nspace.marshal_with(todo_msg_model)
	def put(self, id):
		"""
		[Entirely] Update a todo entity, by specifying the new state of ALL the fields. 
		If the optional 'status' is omitted, it is replaced with default value
		"""
		
		if todo_nspace.payload.get('status', None) is None:
			todo_nspace.payload['status'] = Status().default
		todo = TodoDAO.update(id, todo_nspace.payload)
		if todo is None:
			raise TodoDoesNotExistException("Task with ID {id_} doesn't exist".format(id_=id))
		else:
			return {
					"data": todo,
					"message": "Task was updated as follows"
					}, 200

	
	@require_accesslevel(ACCESS_SCOPE.get('readwrite'))
	@todo_nspace.response(200, "Task was updated as follows + { udpated task details }")
	@todo_nspace.response(404, "Task with ID {id} doesn't exist")
	@todo_nspace.marshal_with(todo_msg_model)
	def patch(self, id):
		"""
		[Partially] Update a todo entity, by specifying ONLY the fields to be modified
		"""

		payload = TodoPatch_Parser.parse_args()
		todo = TodoDAO.patch_update(id, payload)
		if todo is None:
			raise TodoDoesNotExistException("Task with ID {id_} doesn't exist".format(id_=id))
		else:
			return {
					"data": todo,
					"message": "Task was updated as follows"
					}, 200