"""
Creates and registers all todo related and models
Creates a namespace and bind to it
"""

from flask_restplus import Namespace, Model, fields


# Create the namespace
todo_nspace = Namespace('todo', description='Todo operations')


todo = Model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})