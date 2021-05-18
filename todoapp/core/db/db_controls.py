import sqlite3
import click
import os
from flask import current_app, g
from flask.cli import with_appcontext

def connect_db():
	"""
	A 'memoized' implementation that connects to DB if not already connected,
	stores the connection in global context for current request and
	returns the connection handle in either case 
	Additionally, instructs SQLite to retrieve 'dict()' like rows
	for queries for easy data-handling
	"""

	if 'db_conn' not in g:
		g.db_conn = sqlite3.connect(
			current_app.config['DB_PATH'],
			detect_types=sqlite3.PARSE_DECLTYPES
		)
		g.db_conn.row_factory = sqlite3.Row
	return g.db_conn


def close_db(exceptions=None):
	"""
	Closes the DB connection for current request
	if connection was ever made
	"""

	db_conn = g.get('db_conn', None)
	if db_conn is not None:
		db_conn.close()


def get_ordered_migrations():
	"""
	Returns an ordered list of migrations
	in chronological order of schem modification
	"""
	migration_nums = [
		int(script_parts[1]) for script_parts in map(
			lambda x:x.split('.'),
			os.listdir(current_app.config['DB_MIGRATIONS_PATH'])
			)
		if script_parts[-1]=='sql'
	]
	migrations = [
		'.'.join(
			['script', str(serial), 'sql']
		) for serial in sorted(migration_nums)
	]
	return migrations


def refresh_schema():
	"""
	Deletes all tables (truncating entries)
	and instantiate a fresh empty database
	Runs all migrations in chronological order
	"""

	db_conn = connect_db()
	migrations = get_ordered_migrations()
	for script in migrations:
		with current_app.open_resource(
			os.path.join(
				current_app.config['DB_MIGRATIONS_PATH'], 
				script
				)
			) as fin:
			db_conn.executescript(fin.read().decode('utf8'))


@click.command('refresh-db')
@with_appcontext
def make_fresh_schema_cli():
	"""
	Binds the CLI command `refresh-db`
	to clear the database and re-create the schema 
	"""

	refresh_schema()
	click.echo("Database cleared. Schema reloaded")


def init_db_context(app):
	"""
	Registers the `refresh-db` command to CLI
	Attaches close_db to teardown_request signal
	"""

	app.cli.add_command(make_fresh_schema_cli)
	app.teardown_request(close_db)
