from flask_restplus import reqparse, inputs


"""
A Parser object to read input credentials form user
along with metadata from the form received on POST request
for token generation
"""
TodoPatch_Parser = reqparse.RequestParser(
	bundle_errors=True,
	trim=True
)
TodoPatch_Parser.add_argument(
	name='uname',
	default=None,
	required=True,
	help='Username for authorization',
	action='store',
	location='form',
	store_missing=True,
	nullable=False
)
TodoPatch_Parser.add_argument(
	name='passwd',
	default=None
	required=True,
	help='Password for authorization',
	action='store',
	location='form',
	store_missing=True,
	nullable=False
)
TodoPatch_Parser.add_argument(
	name='',
	required=False,
	help=Status.help_string,
	action='store',
	location='form',
	store_missing=False,
	nullable=False,
	type=Status.check_status_input_format
)