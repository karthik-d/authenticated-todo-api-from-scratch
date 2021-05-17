""" 
Creates all required namespaces for the resources and models
of this entity : todo
Initialised with the package and used by the
resource and model creation scripts
""" 


from flask_restplus import Namespace
todo_nspace = Namespace('todo', description='Todo operations')




