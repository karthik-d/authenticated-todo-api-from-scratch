"""
Views for authorization for token grant
"""

import os
import json

from flask import (
	render_template, 
	request, redirect, 
	current_app, 
	make_response, 
	jsonify
)
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from todoapp.core.dao.token import Token as TokenDAO
from todoapp.core.utils.auth import ( 
	ACCESS_SCOPE_REV,
	get_best_scope, 
	validate_client, 
	validate_admin
)
from todoapp.core.utils.generic import add_queries_to_url
from todoapp.api.auth.exception import (
	TokenCreationDeniedException, 
	DidNotCreateTokenException
)
from .request_parser import Credentials_Parser
from .authpages import blueprint as auth_bprint


class AuthorizationView(MethodView):
	methods = [ 'GET', 'POST' ]

	def get(self):
		"""
		Validate OAuth token-creation request URL
		Translate scope to numeric best scope
		Render Credential Verification page
		Receives a POST request with FORM data
		"""
	
		response_type = request.args.get('response_type')
		print(request.args)		
		if response_type != 'token':
			return make_response(
				jsonify({
					'error' : 'Unexpected response type. Expected OAuth2 Implicit-Flow'
					}), 400
			)

		scopes_reqd = request.args.get('scope', '').split()
		best_scope = get_best_scope(scopes_reqd)
		if best_scope == -1:
			return make_response(
				jsonify({
					'error' : 'No valid scopes specified for new token'
					}), 400
			)

		client_id = request.args.get('client_id')
		if not validate_client(client_id):
			return make_response(
				jsonify({
					'error' : 'Unknown client'
					}), 401
			)

		state = request.args.get('state')
		redirect_uri = request.args.get('redirect_uri')
		return render_template(
			'login.html', 
			state=state, 
			redirect=redirect_uri, 
			scope=best_scope
			)


	def post(self):
		"""
		Create an authorization token and revert to redirection URL 
		with access-token
		Receives a POST request with FORM data
		"""

		try:
			payload = Credentials_Parser.parse_args()
		except BadRequest:
			return make_response(
				jsonify({
					'error' : 'Invalid request URL'
					}), 400
			)
		if not validate_admin(payload):
			raise TokenCreationDeniedException("Not authorized to create token")
		token_row = TokenDAO.create(payload)
		if token_row is None:
			raise DidNotCreateTokenException("Could not create the token")
		else:
			redirect_url = payload.get('redirect')
			state = payload.get('state')
			token_row = dict(token_row)
			token_code = token_row.get('token')
			token_scope = token_row.get('scope')

			"""
			THE Ideal Response
			that would be sent to any API-client Server
			that was successfully authorized using
			the OAuth2 Implicit-Flow scheme
			They woudl attach token to the auth header

			encoded_url = add_queries_to_url(
				redirect_url,
				state=state ,
				token=token_code
			)
			return redirect(encoded_url)

			The following is the modified response
			to requests made manually for testing
			purposes. The token code is manually
			attached to the request header
			"""

			return make_response(
				jsonify({
					'token' : token_code,
					'scope' : ACCESS_SCOPE_REV.get(token_scope)
				})
			)

auth_bprint.add_url_rule('/authorize', view_func=AuthorizationView.as_view('authorize_view'))
