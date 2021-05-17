"""
Data Access Object (DAO) Classes for todo
to interface between the 
Database and Data-Requests
"""


class TodoDAO(object):
	
	def __init__(self):
		self.counter = 0
		self.todos = []

	def get(self, id):
		for todo in self.todos:
			if todo['id'] == id:
				return todo
		api.abort(404, "Todo {} doesn't exist".format(id))

	def create(self, data):
		todo = data
		todo['id'] = self.counter = self.counter + 1
		self.todos.append(todo)
		return todo

	def update(self, id, data):
		todo = self.get(id)
		todo.update(data)
		return todo

	def delete(self, id):
		todo = self.get(id)
		self.todos.remove(todo)
	

# Sample data to test the API
DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': '?????'})
DAO.create({'task': 'profit!'})
