import bottle
from bottle.ext.resource import resource_module

app = bottle.Bottle()

import rest_module
import rest_class

resource_module('/with_module', app, rest_module)
rest_class.ExampleResource('/with_class', app)

app.run()
