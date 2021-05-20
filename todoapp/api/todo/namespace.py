from flask_restplus import Namespace

from todoapp.core.utils.auth import AUTH_SPEC

# Create the namespace
todo_nspace = Namespace(
	'todo', 
	description='Todo operations',
	authorizations=AUTH_SPEC
)