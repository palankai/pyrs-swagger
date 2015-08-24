class Swagger(dict):
    title = None
    version = None
    host = None
    base_path = None
    default_response = {'description': 'successful response'}

    def __init__(self, **config):
        super(Swagger, self).__init__({
            'swagger': '2.0',
            'info': {
                'title': config.pop('title', self.title),
                'version': config.pop('version', self.version),
            },
            'paths': {}
        })
        assert self['info'].get('title'), 'Title have to be specified'
        assert self['info'].get('version'), 'Version have to be specified'
        self.setup(config)

    def setup(self, config):
        """
        Setup configuration values
        """
        _setup_value(self, config, 'host', 'host')
        _setup_value(self, config, 'base_path', 'basePath')

    def add(self, base_path, path, methods, **options):
        full_path = base_path+path
        if full_path not in self['paths']:
            self['paths'][full_path] = {}

        for method in methods:
            if method.lower() not in self['paths'][full_path]:
                self['paths'][full_path][method.lower()] = {
                    'responses': {
                        'default': self.default_response
                    }
                }


def _setup_value(data, config, key, *target):
    """Update the `data` deep in the target.
    if the target contains multiple element that will be threated as path
    in data
    """
    value = config.get(key, getattr(data, key))
    if value:
        path = list(target)
        while len(path) > 0:
            key = path.pop(0)
            if len(path):
                if key not in data:
                    data[key] = {}
                data = data[key]
        data[key] = value
