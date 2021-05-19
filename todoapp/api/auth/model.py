from flask_restplus import fields

from .namespace import auth_nspace


TOKEN = auth_nspace.model('Todo',
	{
		'id': fields.Integer(
			readonly=True,
			description='A unique identifier for the token (Auto-Generated)',
			attribute='id'
			),
		'token': fields.String(
			required=True, 
			description='A unique 10-character string',
			attribute='task'
			),
		'read_only': fields.Boolean(
			required=True,
			description='Boolean 1 if read-only, 0 if read-write',
			attribute='read_only'
			)
	}
)

EXCEPTION = todo_nspace.model('TodoException',
	{
		'HTTP_status': fields.Integer(
			description='The HTTP status code for the response',
			attribute='http_code'
		),
		'message': fields.String(
			description='Description of the error/exception',
			attribute='message'
		)
	}
)