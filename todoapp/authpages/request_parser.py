from flask_restplus import reqparse, inputs


"""
A Parser object to read input credentials form user
along with metadata from the form received on POST request
for token generation
"""
Credentials_Parser = reqparse.RequestParser(
	bundle_errors=True,
	trim=True
)
Credentials_Parser.add_argument(
	name='uname',
	default=None,
	required=True,
	help='Username for authorization',
	action='store',
	location='form',
	store_missing=True,
	nullable=False,
	dest='username'
)
Credentials_Parser.add_argument(
	name='passwd',
	default=None,
	required=True,
	help='Password for authorization',
	action='store',
	location='form',
	store_missing=True,
	nullable=False,
	dest='password'
)
Credentials_Parser.add_argument(
	name='scope',
	required=False,
	help='Boolean 1 if read-only, 0 if read-write',
	action='store',
	location='form',
	store_missing=False,
	nullable=False,
	type=inputs.int_range(low=0, high=2),
	dest='scope'
)
Credentials_Parser.add_argument(
	name='redirect',
	required=True,
	help='Redirect URL to return token',
	action='store',
	location='form',
	store_missing=False,
	nullable=False,
	dest='redirect'
)
Credentials_Parser.add_argument(
	name='state',
	required=True,
	help='CSRF prevention string',
	action='store',
	location='form',
	store_missing=False,
	nullable=False,
	dest='state'
)