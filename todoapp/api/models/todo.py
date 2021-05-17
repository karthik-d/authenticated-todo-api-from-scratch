"""
Creates and registers all todo related models
to the todo namespace
"""

from flask_restplus import fields

from api import todo_nspace


todo = todo_nspace.model('Todo', {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')
})