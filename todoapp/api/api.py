""" 
Creates the API blueprint for this package
Registers all required namespaces to the blueprint
"""

from flask import Blueprint
from flask_restplus import Api
from jsonschema import FormatChecker

from .auth import AUTH_SPEC
from .auth.namespace import auth_nspace
from .todo.namespace import todo_nspace
from .todo.custom_fields import Status


blueprint = Blueprint('api', __name__)

format_checker = FormatChecker()
format_checker.checks(Status.__schema_format__, Status.format_violation) (Status.check_status_input_format)

API = Api(
	blueprint,
    title='Todo App API',
    version='1.0',
    description='A quick endpoint to manage your todos',
	format_checker = format_checker,
	authorizations=AUTH_SPEC
)

API.add_namespace(todo_nspace, path='/todo')
API.add_namespace(auth_nspace, path='/api-auth')