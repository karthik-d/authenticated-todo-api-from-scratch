"""
Creates and registers all todo related models and request parsers
Creates a namespace and bind to it
"""

from flask_restplus import Model, fields, reqparse, inputs

from .namespace import todo_nspace
from .custom_fields import Status


"""
MODEL definitions
"""
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
				),
		'due_by': fields.Date(
				dt_format='iso8601',
				required=True,
				description='Due date for the task',
				attribute='due_by',
				),
		'status': Status(
				default='Not started',
				description='Completion status of the task',
				attribute='status'
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
		'Exception': fields.Nested(
					EXCEPTION,
					description='Exception code and message',
					attribute='exception'
				),
		'Associated Data': fields.Nested(
					TODO,
					description='Associated todos for the exception',
					attribute='data'
				)
	}
)


"""
Request-Parsers definitions
"""
todopatch_parser = reqparse.RequestParser()
todopatch_parser.add_argument(
	name='task',
	required=False,
	help='Task description as text',
	action='store',
	location='json',
	store_missing=False,
	trim=True,
	nullable=False
)
todopatch_parser.add_argument(
	name='due_by',
	required=False,
	help='Due date in (yyyy-mm-dd) format',
	action='store',
	location='json',
	store_missing=False,
	trim=True,
	nullable=False,
	type=inputs.date_from_iso8601
)
todopatch_parser.add_argument(
	name='status',
	required=False,
	help=Status.help_string,
	action='store',
	location='json',
	store_missing=False,
	trim=True,
	nullable=False,
	type=Status.check_status_input_format
)

