
class ApplicationConfig:
	DEBUG = True
	DB_NAME = 'TodoApp.sqlite'
	API_NAME = 'Todo App API'
	# Disable additional error messages from flask backend for 404
	ERROR_404_HELP = False
	TRAP_HTTP_EXCEPTIONS = True
	PROPAGATE_EXCEPTIONS = True
