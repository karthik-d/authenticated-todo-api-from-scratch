"""
Creates and registers all todo related and models
Creates a namespace and bind to it
"""

from flask_restplus import Namespace, Model, fields


# Create the namespace
todo_nspace = Namespace('todo', description='Todo operations')


todo = Model('Todo', 
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

exception = Model('TodoException',
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