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
        self.context = config.pop('context', None)
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

        self._add_operations(self['paths'][full_path], methods, options)

    def _add_operations(self, base, methods, options):
        for method in methods:
            base[method.lower()] = self._get_operation(options)

    def _get_operation(self, options):
        operation = {
            'responses': self._get_responses(options)
        }
        if 'name' in options:
            operation['operationId'] = options['name']
        parameters = self._get_parameters(options)
        if parameters:
            operation['parameters'] = parameters
        return operation

    def _get_responses(self, options):
        schema = options.get('response')
        status = options.get('status', 200)
        headers = options.get('response_headers', {})
        if not schema:
            return {'default': self.default_response}
        response = {'schema': schema.get_jsonschema(context=self.context)}
        if headers:
            response['headers'] = {}
            for key, header in headers:
                response['headers'][key] = \
                    header.get_jsonschema(context=self.context)
        return {
            status: response
        }

    def _get_parameters(self, options):
        request = options.get('request')
        query = options.get('query', {})
        headers = options.get('headers', {})
        path = options.get('params', {})
        parameters = []
        for key, schema in path.items():
            parameters.append(self._get_parameter('path', key, schema))
        if request:
            parameters.append({
                'in': 'body',
                'name': 'body',
                'required': True,
                'schema': request.get_jsonschema(context=self.context)
            })
        for key, schema in query.items():
            parameters.append(self._get_parameter('query', key, schema))
        for key, schema in headers.items():
            parameters.append(self._get_parameter('headers', key, schema))
        return parameters

    def _get_parameter(self, in_, name, schema):
        param = {
            'in': in_,
            'name': name,
            'required': schema.get_attr('required', False),
        }
        param.update(schema.get_jsonschema(context=self.context))
        return param


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
