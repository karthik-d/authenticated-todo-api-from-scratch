from flask_restplus import Resource

from .namespace import auth_nspace 
from .model import TOKEN as token_model
from .request_parser import Credentials_Parser
from .exception import DidNotCreateTokenException


@auth_nspace.route(
	'/token', 
	methods=[ 'POST' ],
	endpoint='auth-token'
)
class Token(Resource):	

	#@todo_nspace.doc('create_todo')
	#@todo_nspace.response(201, "Following tasks were added to the todo list + { created tasks' details }")
	#@todo_nspace.response(500, "Could not create task")
	@auth_nspace.marshal_list_with(token_model)
	def post(self):
		"""
		Create an authorization token
		Receives a POST request with FORM data
		"""

		payload = Credentials_Parser.parse_args()
		if not validate_admin(payload):
			raise TokenCreationDeniedException("Not authorized to create token")
		token_row = TodoDAO.create(payload)
		if token_row is None:
			raise DidNotCreateTokenException("Could not create task")
		else:
			return token_row, 201
