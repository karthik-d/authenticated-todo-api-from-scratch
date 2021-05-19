"""
Creates and registers all todo related Request-Parser definitions
"""

from flask_restplus import reqparse, inputs

from .custom_fields import Status


"""
A Parser object to read partial subset of fields for a todo entity
One or more of 'task', 'due_by' and 'status' will be accepted
"""
TodoPatch_Parser = reqparse.RequestParser(
	bundle_errors=True,
	trim=True
)
TodoPatch_Parser.add_argument(
	name='task',
	required=False,
	help='Task description as text',
	action='store',
	location='json',
	store_missing=False,
	nullable=False
)
TodoPatch_Parser.add_argument(
	name='due_by',
	required=False,
	help='Due date in (yyyy-mm-dd) format',
	action='store',
	location='json',
	store_missing=False,
	nullable=False,
	type=inputs.date_from_iso8601
)
TodoPatch_Parser.add_argument(
	name='status',
	required=False,
	help=Status.help_string,
	action='store',
	location='json',
	store_missing=False,
	nullable=False,
	type=Status.check_status_input_format
)


"""
A Parser object to read date_field from URL arguments
"""
DateArg_Parser = reqparse.RequestParser(
	bundle_errors=True,
	trim=True
)
DateArg_Parser.add_argument(
	name='due_date',
	required=False,
	help='Due date in (yyyy-mm-dd) format',
	action='store',
	location='args',
	store_missing=False,
	nullable=False,
	type=inputs.date_from_iso8601
)