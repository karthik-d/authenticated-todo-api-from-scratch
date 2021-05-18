"""
Creates and registers all todo related and models
Creates a namespace and bind to it
"""

from flask_restplus import Namespace, Model, fields


# Create the namespace
todo_nspace = Namespace('todo', description='Todo operations')


TODO = todo_nspace.model('Todo', 
	{
		'id': fields.Integer(
				readonly=True,
				description='The task unique identifier',
				attribute='id'
				),
		'task': fields.String(
				required=True, 
				description='The task details',
				attribute='task'
				)
	}
)

TODO_WITH_MESSAGE = todo_nspace.model('TodoWithMessage',
	{
		'message': fields.String(
				description='Description of what was was done due to the request',
				attribute='message'
				),
		'todos': fields.Nested(
				TODO,
				description='Associated todos for the response',
				attribute='data'
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


EXCEPTION_WITH_DATA = todo_nspace.model('TodoExceptionWithData',
	{
		'Exception': fields.Nested(EXCEPTION),
		'Associated Data': fields.Nested(TODO)
	}
)