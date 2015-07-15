from bottle.ext.resource import BottleResource


class ExampleResource(BottleResource):

    def prepare(self):
        self.pk_regex = '[0-9]+'

    def additional_routes(self):
        return [
            ['/other_route', 'GET', self.other_route],
        ]

    def index(self):
        return 'Hello world with class'

    def show(self, pk):
        return 'Hello primary key #%s with class' % pk

    def other_route(self):
        return 'Hello with other route into the class'

if __name__ == '__main__':
    import bottle
    app = bottle.Bottle()
    ExampleResource('/with_class', app).run()
