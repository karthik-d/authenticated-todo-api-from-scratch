from flask import Blueprint
from flask_restplus import Api

from .todo import todo_nspace

blueprint = Blueprint('api', __name__)

API = Api(
	blueprint,
    title='Todo App API',
    version='1.0',
    description='A quick endpoint to manage your todos'
)

API.add_namespace(todo_nspace, path='/todo')