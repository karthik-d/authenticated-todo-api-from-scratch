"""
Creates and registers all todo related resources
to the todo namespace
"""

from flask_restplus import Resource

from todoapp.core.todo_dao import DAO
from api import todo_nspace


@todo_nspace.route('/')
class TodoList(Resource):

    @todo_nspace.doc('list_todos')
    @todo_nspace.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @todo_nspace.doc('create_todo')
    @todo_nspace.expect(todo)
    @todo_nspace.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@todo_nspace.route('/<int:id>')
@todo_nspace.response(404, 'Could not find that todo')
@todo_nspace.param('id', 'The task ID (unique) ')
class Todo(Resource):
	
    @todo_nspace.doc('get_todo')
    @todo_nspace.marshal_with(todo)
    def get(self, id):
        return DAO.get(id)

    @todo_nspace.doc('delete_todo')
    @todo_nspace.response(204, 'Todo deleted')
    def delete(self, id):
        DAO.delete(id)
        return '', 204

    @todo_nspace.expect(todo)
    @todo_nspace.marshal_with(todo)
    def put(self, id):
        return DAO.update(id, api.payload)