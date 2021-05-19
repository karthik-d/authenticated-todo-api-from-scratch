"""
Data Access Object (DAO) Classes for api-token
to interface between the 
Database and Data-Requests
"""

import sqlite3

from todoapp.core.utils.auth import generate_token
from .base import DAOBase


class Token(DAOBase):
	
	def __init__(self, *args, **kwargs):
		super(Todo, self).__init__(*args, **kwargs)


	@classmethod
	def get_by_id(cls, id_):
		"""
		Retrieves a token row by id
		Returns a list of 'sqlite3 Row objects'
		"""

		query_string = """
			SELECT *
			FROM token
			WHERE id = :id_
		"""
		result = cls.exec_retrieve(query_string, id_=id_)
		return result.fetchone()


	@classmethod
	def create(cls, data):
		"""
		Creates a new token with specified access
		While UUID has near-zero chance of duplication,
		if duplication does occurs, it regenerates the token
		"""

		update_string = """
			INSERT INTO token (token, scope)
			VALUES (:token, :scope)
		"""

		scope = data.get('scope')
		while True:
			try:
				token = generate_token()
				resp_cursor = cls.exec_update(
					update_string,
					token=token,
					scope=scope
				)
			except sqlite3.IntegrityError:
				continue
			else:
				break

		if resp_cursor.rowcount==0:
			return None 
		else:
			inserted_id = resp_cursor.lastrowid
			return cls.get_by_id(inserted_id)