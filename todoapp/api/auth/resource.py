from flask_restplus import Resource

from todoapp.core.utils.auth import validate_admin
from todoapp.core.dao.token import Token as TokenDAO
from .namespace import auth_nspace 
from .model import TOKEN as token_model
from .request_parser import Credentials_Parser

from todoapp.api.auth import (
	ACCESS_SCOPE, 
	require_token,
	require_accesslevel
)

from .exception import (
	DidNotCreateTokenException,
	TokenCreationDeniedException,
	EmptyTokenListException,
	TokenDoesNotExistException
)


@auth_nspace.route(
	'/token', 
	methods=[ 'GET', 'POST' ],
	endpoint='auth-tokens'
)
class TokenList(Resource):	

	@require_accesslevel(ACCESS_SCOPE.get('admin'))
	@auth_nspace.doc('list_tokens')
	@auth_nspace.response(200, "{ tokens list } OR No active tokends for the API")
	@auth_nspace.marshal_with(token_model)
	def get(self):
		"""
		Display all active tokens for the API
		"""

		tokens = TokenDAO.all()
		if not tokens:
			raise EmptyTodoListException("No active tokens for the API")
		else:
			return tokens, 200


	@auth_nspace.doc('create_token')
	@auth_nspace.response(201, "Token was created")
	@auth_nspace.response(500, "Could not create token")
	@auth_nspace.marshal_list_with(token_model)
	def post(self):
		"""
		Create an authorization token
		Receives a POST request with FORM data
		"""

		payload = Credentials_Parser.parse_args()
		if not validate_admin(payload):
			raise TokenCreationDeniedException("Not authorized to create token")
		token_row = TokenDAO.create(payload)
		if token_row is None:
			raise DidNotCreateTokenException("Could not create task")
		else:
			return token_row, 201


@auth_nspace.route(
	'/token/<int:id>', 
	methods=[ 'GET' ],
	endpoint='auth-token'
)
class Token(Resource):	

	@require_accesslevel(ACCESS_SCOPE.get('admin'))
	@auth_nspace.doc('get_token')
	@auth_nspace.response(200, "{ requested token }")
	@auth_nspace.response(404, "Token with ID {id} doesn't exist")
	@auth_nspace.marshal_with(token_model)
	def get(self, id):
		"""
		Display id-speicified token for the API
		"""

		token = TokenDAO.get_by_id(id)
		if token is None:
			raise TokenDoesNotExistException("Token with ID {id_} doesn't exist".format(id_=id))
		else:
			return token, 200
