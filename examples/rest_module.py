import bottle

app = bottle.Bottle()


def index():
    return 'Hello World with module'


def show(pk):
    return 'Hello primary key #%s with module' % pk


@app.route('/other_route', 'GET')
def other_route():
    return 'Hello world with other route into de module'

if __name__ == '__main__':
    import sys
    from bottle.ext.resource import resource_module
    root = bottle.Bottle()
    resource_module('/with_module', root, sys.modules[__name__]).run()
