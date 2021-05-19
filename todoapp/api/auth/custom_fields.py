"""
CUSTOM fields for token related models
Includes validations that will be linked to 
the namespace.expect() validators
Adds the 'schema_format' to the FormatChecker of Api class
Class input-validate method is also used for Request-Parser validation
"""

from flask_restplus import fields

from .namespace import auth_nspace


class Scope(fields.String):
	"""
	Custom field to store the status of a token
	Must be one of ( 'Not started', 'In progress', 'Finished' )
	-> Case-INsensitive for input validation ( from request body )
	-> Spaces NOT necessay for input validation ( from request body )
	Performs Marshalling-Validation in format finction
	Performs Input-Validation by registering 'check_status_input' to API's Format Checker
	"""

	__schema_format__ = 'token_scope'

	format_violation = ValueError

	representation = {
		0 : 'Read-Only',
		1 : 'Read-Write',
		2 : 'Admin'
	}

	help_string = "\
	Scope of the token must be one of ( {scopes} ) representing ( {vals} ).".format(
		scopes = ", ".join(map(str, representation.keys())),
		vals = ", ".join(representation.values())
	).strip()


	def __init__(self, *args, **kwargs):
		super(Scope, self).__init__(*args, **kwargs)


	def format(self, value):
		"""
		Add to the 'format' of String field
		to enforce validation of string presence in 
		allowed choices
		"""

		value = super(Scope, self).format(value)

		if value is None:
			return None 

		if isinstance(value, str):
			value = int(value)
		
		if value not in range(0, 3):
			raise fields.MarshallingError(Scope.format_violation)
		else:
			return Scope.representation[value] 
			



	