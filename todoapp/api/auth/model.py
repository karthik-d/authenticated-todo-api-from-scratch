from flask_restplus import fields

from .namespace import auth_nspace


TOKEN = todo_nspace.model('Todo',
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