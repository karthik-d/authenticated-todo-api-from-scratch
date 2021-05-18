""" 
Creates and registers resources
Binds the models to the namespace
of this entity : todo
Initialised with the package
""" 

from flask_restplus import Namespace

from .model import *
from .resource import *
from .exception import *
