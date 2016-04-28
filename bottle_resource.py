import os
from uuid import uuid1
import bottle
from bottle import tob, template, ERROR_PAGE_TEMPLATE, abort


class Format(object):
    INT = '[0-9]+'
    OID = '^[a-f-0-9]{24}$'
    UUID = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'


def uuid(node=None, clock_seq=None):
    return str(uuid1(node, clock_seq))


def resource_module(path, root_app, module):
    app = module.app if 'app' in module.__dict__ else bottle.Bottle()
    app.install(JSONPlugin())
    pk = module.PK if 'PK' in module.__dict__ else '<pk:re:%s>' % Format.UUID

    if 'index' in module.__dict__:
        app.route('/', 'GET', callback=module.index)

    if 'new' in module.__dict__:
        app.route('/new', 'GET', callback=module.new)

    if 'create' in module.__dict__:
        app.route('/', 'POST', callback=module.create)

    if 'edit' in module.__dict__:
        app.route('/%s/edit' % pk, 'GET', callback=module.edit)

    if 'show' in module.__dict__:
        app.route('/%s' % pk, 'GET', callback=module.show)

    if 'partial_update' in module.__dict__:
        app.route('/%s' % pk, 'PATCH', callback=module.partial_update)

    if 'update' in module.__dict__:
        app.route('/%s' % pk, 'PUT', callback=module.update)

    if 'destroy' in module.__dict__:
        app.route('/%s' % pk, 'DELETE', callback=module.destroy)

    root_app.mount(path, app)

    return root_app


class JSONPlugin(object):
    ''' Bottle plugin which encapsulates results and error in a json object.
    Intended for instances where you want to use Bottle as an api server. '''

    name = 'json'
    api = 2

    def __init__(self, ensure_ascii=False, **kwargs):
        try:
            import simplejson as json
        except ImportError:
            import json
        finally:
            try:
                from bson.json_util import _json_convert
                dumps = lambda obj, *args, **kwargs: json.dumps(
                    _json_convert(obj), *args, **kwargs
                )
            except ImportError:
                dumps = json.dumps

        self.dumps = lambda obj: dumps(obj, ensure_ascii, **kwargs)

    def accept(self, content_type):
        header_accept = bottle.request.headers.get('Accept', '')
        header_ct = bottle.request.headers.get('Content-Type', '')

        if isinstance(content_type, basestring):
            if content_type in header_accept or content_type in header_ct:
                return True
        elif isinstance(content_type, (list, tuple)):
            for ct in content_type:
                if ct in header_accept or ct in header_ct:
                    return True
        return False

    def setup(self, app):
        self.app = app
        if self.app.config.autojson:
            self.app.uninstall('json')
        ''' Handle plugin install '''
        setattr(self.app, 'default_error_handler', self.custom_error_handler)

    def apply(self, callback, route):
        ''' Handle route callbacks '''
        if not self.dumps:
            return callback

        def wrapper(*a, **ka):
            ''' Monkey patch method accept in thread_local request '''
            setattr(bottle.request, 'accept', getattr(self, 'accept'))
            ''' Encapsulate the result in json '''
            output = callback(*a, **ka)
            if bottle.request.accept('json'):
                if bottle.response.status_code in bottle.HTTP_CODES:
                    status = bottle.HTTP_CODES[bottle.response.status_code]
                else:
                    status = 'Unknow'
                response_object = {
                    'status': status,
                    'code': bottle.response.status_code,
                    'response': output,
                    'error': None
                }
                bottle.response.content_type = 'application/json'
                return self.dumps(response_object)
            return output
        return wrapper

    def custom_error_handler(self, error):
        if self.accept('json'):
            ''' Monkey patch method for json formatting error responses '''
            response_object = {
                'code': error.status_code,
                'status': error.body,
                'response': None,
                'error': True
            }
            if bottle.DEBUG and error.traceback:
                response_object['debug'] = {
                    'exception': repr(error.exception),
                    'traceback': repr(error.traceback),
                }
            bottle.response.content_type = 'application/json'
            return self.dumps(response_object)
        return tob(template(ERROR_PAGE_TEMPLATE, e=error))


class BottleResource(object):
    def __init__(self, root_path, root_app, **kwargs):
        self._root_app = root_app
        self._root_path = root_path
        self._app = bottle.Bottle()
        self._app.install(JSONPlugin())
        self.pk = kwargs.pop('pk', '<pk:re:%s>' % Format.UUID)
        self.prepare(**kwargs)
        self._routes()
        self._additional_routes()
        self._root_app.mount(self._root_path, self._app)

    def _routes(self):
        pk = self.pk
        self._app.route('/', 'GET', callback=self.index)
        self._app.route('/new', 'GET', callback=self.new)
        self._app.route('/', 'POST', callback=self.create)
        self._app.route('/%s/edit' % pk, 'GET', callback=self.edit)
        self._app.route('/%s' % pk, 'GET', callback=self.show)
        self._app.route('/%s' % pk, 'PATCH', callback=self.partial_update)
        self._app.route('/%s' % pk, 'PUT', callback=self.update)
        self._app.route('/%s' % pk, 'DELETE', callback=self.destroy)

    def _additional_routes(self):
        for i in self.additional_routes():
            self._app.route(i[0], i[1], callback=i[2])

    def additional_routes(self):
        return []

    @property
    def app(self):
        return self._app

    def prepare(self, **kwargs):
        pass

    def index(self):
        abort(404)

    def new(self):
        abort(404)

    def create(self):
        abort(404)

    def edit(self, *args):
        abort(404)

    def show(self, *args):
        abort(404)

    def partial_update(self, *args):
        abort(404)

    def update(self, *args):
        abort(404)

    def destroy(self, *args):
        abort(404)

    def run(self, host='0.0.0.0', port=8080):
        self._root_app.run(host=host, port=os.environ.get('PORT', port))
