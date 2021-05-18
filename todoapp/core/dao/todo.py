"""
Data Access Object (DAO) Classes for todo
to interface between the 
Database and Data-Requests
"""

from .base import DAOBase


class Todo(DAOBase):
	
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
		if resp_cursor.rowcount==0:
			return None 
		else:
			inserted_id = resp_cursor.lastrowid
			return cls.get(inserted_id)

	@classmethod
	def update(cls, id_, data):
		update_string = """
			UPDATE
				todo
			SET
				task = :task
			WHERE 
				id = :id_
		"""
		todo_task = data.get('task')		
		resp_cursor = cls.exec_update(update_string, id_=id_, task=todo_task)
		print(resp_cursor.rowcount)
		if resp_cursor.rowcount==0:
			return None 
		else:
			return cls.get(id_)

	@classmethod
	def delete(cls, id_):
		update_string = """
			DELETE
			FROM todo
			WHERE id = :id_
		"""
		resp_cursor = cls.exec_update(update_string, id_=id_)
		if resp_cursor.rowcount==0:
			return None
		else:
			return id_
	
