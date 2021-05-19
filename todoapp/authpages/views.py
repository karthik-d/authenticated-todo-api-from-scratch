"""
Views for authourization for token grant
"""

import os

from flask import render_template, request, redirect
from flask.views import MethodView

from .authpages import blueprint as auth_bprint
import json


class AuthorizationView(MethodView):
	methods = [ 'GET', 'POST' ]

	def get(self):
		scopes = request.args.get('scope', '').split()
		return render_template('login.html', redirect_url=redirect_url)

	def post(self):
		print(request.form)
		redirect_url = request.form.get('redirect_url')
		return redirect(redirect_url)

auth_bprint.add_url_rule('/authorize', view_func=AuthorizationView.as_view('authorize_view'))
