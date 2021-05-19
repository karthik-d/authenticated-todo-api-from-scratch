from flask_restplus import Namespace


# Create the namespace
auth_nspace = Namespace(
	'auth', 
	description='Authorization for API operations'
)