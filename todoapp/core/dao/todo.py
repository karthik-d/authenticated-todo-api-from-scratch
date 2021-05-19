"""
Data Access Object (DAO) Classes for todo
to interface between the 
Database and Data-Requests
"""

from datetime import date

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
		By default, they are ordered by the due-date
		"""

		query_string = """
			SELECT * 
			FROM todo
			ORDER BY due_by
		"""
		result = cls.exec_retrieve(query_string)
		return result.fetchall()

	@classmethod
	def overdue(cls):
		"""
		Retrieves overdue task rows from the 'todo' relation
		An overdue task is "due before today" and "unfinished"
		Returns a list of 'sqlite3 Row objects'
		By default, they are ordered by the due-date
		"""

		query_string = """
			SELECT * 
			FROM todo
			WHERE due_by < :date
			  AND status <> "Finished"
			ORDER BY due_by
		"""
		curr_date = date.today().strftime('%Y-%m-%d')
		result = cls.exec_retrieve(query_string, date=curr_date)
		return result.fetchall()

	@classmethod
	def finished(cls):
		"""
		Retrieves finished task rows from the 'todo' relation
		A finished task has status "Finished"
		Returns a list of 'sqlite3 Row objects'
		By default, they are ordered by the due-date
		"""

		query_string = """
			SELECT * 
			FROM todo
			WHERE status = "Finished"
			ORDER BY due_by
		"""
		curr_date = date.today().strftime('%Y-%m-%d')
		result = cls.exec_retrieve(query_string, date=curr_date)
		return result.fetchall()

	@classmethod
	def due_on(cls, due_date):
		"""
		Retrieves unfinished task rows from the 'todo' relation
		that are due on 'due_date'
		Returns a list of 'sqlite3 Row objects'
		"""

		query_string = """
			SELECT * 
			FROM todo
			WHERE due_by = :date
			  AND status <> "Finished"
		"""
		date = due_date.strftime('%Y-%m-%d')
		result = cls.exec_retrieve(query_string, date=date)
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
			INSERT INTO todo (task, due_by, status)
			VALUES (:task, :due, :status)
		"""
		todo_task = data.get('task')
		todo_due = data.get('due_by')
		todo_status = data.get('status')
		resp_cursor = cls.exec_update(
			update_string, 
			task=todo_task,
			due=todo_due,
			status=todo_status
		)
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
				task = :task,
				due_by = :due,
				status = :status
			WHERE 
				id = :id_
		"""
		todo_task = data.get('task')
		todo_due = data.get('due_by')
		todo_status = data.get('status')
		resp_cursor = cls.exec_update(
			update_string, 
			id_=id_,
			task=todo_task,
			due=todo_due,
			status=todo_status
		)
		if resp_cursor.rowcount==0:
			return None 
		else:
			return cls.get(id_)


	@classmethod
	def patch_update(cls, id_, data):
		update_string = """
			UPDATE
				todo
			SET
				{field} = :value
			WHERE 
				id = :id_
		"""
		rowcount = 0
		for field,value in data.items():
			resp_cursor = cls.exec_update(
				update_string.format(field=field),
				value=value,
				id_=id_
			)
			rowcount += resp_cursor.rowcount
		if rowcount==0:
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
	
