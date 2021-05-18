import todoapp.core.db as db

class DAOBase(object):
	
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