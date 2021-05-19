from flask_restplus import Resource

from .namespace import auth_nspace 
from .model import TOKEN as token_model
from .request_parser import Credentials_Parser


@auth_nspace.route(
	'/', 
	methods=[ 'POST' ],
	endpoint='auth-token'
)
class Token(Resource):	

	#@todo_nspace.doc('create_todo')
	#@todo_nspace.response(201, "Following tasks were added to the todo list + { created tasks' details }")
	#@todo_nspace.response(500, "Could not create task")
	@todo_nspace.expect(Credentials_Parser, validate=True)
	@todo_nspace.marshal_list_with(token_model)
	def post(self):
		"""
		Create an authorization token
		Receives a POST request with FORM data
		"""

		todo = TodoDAO.create(todo_nspace.payload)
		if todo is None:
			raise DidNotCreateTodoException("Could not create task")
		else:
			return {
					"data": todo,
					"message": "Following tasks were added to the todo list"
					}, 201
