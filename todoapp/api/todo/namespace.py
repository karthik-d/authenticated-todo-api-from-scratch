from flask_restplus import Namespace

from todoapp.api.auth import AUTH_SPEC, AUTH_NAME


# Create the namespace
todo_nspace = Namespace(
	'todo', 
	description='Todo operations',
	authorizations=AUTH_SPEC
)