"""
CUSTOM fields for todo related models
Includes validations that will be linked to 
the namespace.expect() validators
Adds the 'schema_format' to the FormatChecker of Api class
Class input-validate method is also used for Request-Parser validation
"""

from flask_restplus import fields

from .namespace import todo_nspace


class Status(fields.String):
	"""
	Custom field to store the status of a todo
	Must be one of ( 'Not started', 'In progress', 'Finished' )
	-> Case-INsensitive for input validation ( from request body )
	-> Spaces NOT necessay for input validation ( from request body )
	Performs Marshalling-Validation in format finction
	Performs Input-Validation by registering 'check_status_input' to API's Format Checker
	"""

	__schema_format__ = 'todo_status'

	format_violation = ValueError

	representation = {
		'notstarted': 'Not started',
		'inprogress': 'In progress',
		'finished': 'Finished'
	}

	help_string = "\
	Status of the task must be one of ( {statuses} ). Spaces and Cases can be ignored!".format(
		statuses = ", ".join(representation.values())
	).strip()


	def __init__(self, *args, **kwargs):
		super(Status, self).__init__(*args, **kwargs)
		self.default = Status.representation.get('notstarted')


	def format(self, value):
		"""
		Add to the 'format' of String field
		to enforce validation of string presence in 
		allowed choices
		"""

		value = super(Status, self).format(value)
		if value in (None, 'None'):
			return None 

		value_squeezed = value.replace(' ', '').lower()
		if value_squeezed in Status.representation.keys():
			return Status.representation[value_squeezed] 
		else:
			raise fields.MarshallingError(Status.format_violation)


	@classmethod
	def check_status_input_format(cls, value):
		"""
		Input-validation (format-checking) function for the 'Status' custom-field
		Will be registered to the API's format_checker
		Also used for validation Request-Parser arguments
		"""
		
		value_squeezed = value.replace(' ', '').lower()
		if value_squeezed in cls.representation.keys():
			return cls.representation[value_squeezed] 
		else:
			raise cls.format_violation

	@classmethod 
	def clean(cls, value):
		"""
		Cleans up the value before entry into DB
		The supplied value MUST already be validated as 
		a valid slug. This method merely tranforms it into
		the representation format for storage
		"""

		value_squeezed = value.replace(' ', '').lower()
		return cls.representation[value_squeezed]



	