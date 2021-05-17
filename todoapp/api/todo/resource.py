"""
Creates and registers all todo_model related resources
to the todo_model namespace
"""

from flask_restplus import Resource

from todoapp.core.dao.todo import TodoDAO
from .model import todo_nspace
from .model import todo as todo_model


@todo_nspace.route('/')
class TodoList(Resource):

    @todo_nspace.doc('list_todos')
    @todo_nspace.marshal_list_with(todo_model)
    def get(self):
        '''List all tasks'''
        return TodoDAO.todos

    @todo_nspace.doc('create_todo')
    @todo_nspace.expect(todo_model)
    @todo_nspace.marshal_with(todo_model, code=201)
    def post(self):
        '''Create a new task'''
        return TodoDAO.create(api.payload), 201


@todo_nspace.route('/<int:id>')
@todo_nspace.response(404, 'Could not find that todo_model')
@todo_nspace.param('id', 'The task ID (unique) ')
class todo_model(Resource):
	
    @todo_nspace.doc('get_todo')
    @todo_nspace.marshal_with(todo_model)
    def get(self, id):
        return TodoDAO.get(id)

    @todo_nspace.doc('delete_todo')
    @todo_nspace.response(204, 'todo_model deleted')
    def delete(self, id):
        TodoDAO.delete(id)
        return '', 204

    @todo_nspace.expect(todo_model)
    @todo_nspace.marshal_with(todo_model)
    def put(self, id):
        return TodoDAO.update(id, api.payload)