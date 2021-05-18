"""
Data Access Object (DAO) Classes for todo
to interface between the 
Database and Data-Requests
"""

import sqlite3

import todoapp.core.db as db

class TodoBase_(object):
	
	@classmethod 
	def exec_retrieve(cls, query, **params):
		connection = db.connect_db()
		cursor = connection.cursor()
		return cursor.execute(query, params)

	@classmethod 
	def exec_update(cls, query, **params):
		connection = db.connect_db()
		cursor = connection.cursor()
		response = cursor.execute(query, params)
		connection.commit()
		return response


class Todo(TodoBase_):
	
	def __init__(self):
		self.counter = 0
		self.todos = []

	@classmethod
	def all(cls):
		"""
		Retrieves all rows from the 'todo' relation
		Returns a list of 'sqlite3 Row objects'
		"""

		query_string = """
			SELECT * 
			FROM todo
			ORDER BY id
		"""
		result = cls.exec_retrieve(query_string)
		result.fetchall()
		return result.fetchall()

	@classmethod
	def get(cls, id_):
		query_string = """
			SELECT *
			FROM todo
			WHERE id = :id_
		"""
		result = cls.exec_retrieve(query_string, id_=id_)
		return result.fetchone()

	@classmethod 
	def create(cls, data):
		update_string = """
			INSERT INTO todo (task)
			VALUES (:task)
		"""
		todo_task = data.get('task')
		resp_cursor = cls.exec_update(update_string, task=todo_task)
		if not resp_cursor:
			return None 
		else:
			inserted_id = resp_cursor.lastrowid
			return cls.get(inserted_id)

	def update(self, id, data):
		todo = self.get(id)
		todo.update(data)
		return todo

	def delete(self, id):
		todo = self.get(id)
		self.todos.remove(todo)
	
