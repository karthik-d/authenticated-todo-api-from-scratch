from flask_restplus import Resource

from todoapp.core.utils.auth import ACCESS_SCOPE
from todoapp.core.dao.token import Token as TokenDAO
from .namespace import auth_nspace 
from .model import TOKEN as token_model
from todoapp.api.auth import require_token, require_accesslevel

from .exception import (
	DidNotCreateTokenException,
	TokenCreationDeniedException,
	EmptyTokenListException,
	TokenDoesNotExistException
)


@require_token
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

@require_token
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
