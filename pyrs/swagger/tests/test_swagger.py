import unittest

from .. import swagger
from . import validator


class TestSwaggerBasic(unittest.TestCase):

    def test_build(self):
        doc = swagger.Swagger(title='example', version='1.0')

        self.assertIsInstance(doc, dict)
        validator.validate(doc)

    def test_declared_title_and_version(self):
        class MySwagger(swagger.Swagger):
            title = 'example'
            version = '1.0'

        validator.validate(MySwagger())

    def test_declared_title_and_version_behaviour(self):
        class MySwagger(swagger.Swagger):
            title = 'example'
            version = '1.0'

        doc = MySwagger(title='New Title', version='New version')
        validator.validate(doc)

        self.assertEqual(doc['info']['title'], 'New Title')
        self.assertEqual(doc['info']['version'], 'New version')

    def test_assertion_without_title(self):
        with self.assertRaises(AssertionError):
            swagger.Swagger(version='1.0')

    def test_assertion_without_version(self):
        with self.assertRaises(AssertionError):
            swagger.Swagger(title='example')


class TestExtendingSwagger(unittest.TestCase):

    def test_host(self):
        doc = swagger.Swagger(title='t', version='v', host='localhost')
        validator.validate(doc)

        self.assertEqual(doc['host'], 'localhost')

    def test_base_path(self):
        doc = swagger.Swagger(title='t', version='v', base_path='/api')
        validator.validate(doc)

        self.assertEqual(doc['basePath'], '/api')


class TestAddingPath(unittest.TestCase):

    def test_add(self):
        doc = swagger.Swagger(title='t', version='v')
        doc.add('/users', '/', ['GET', 'POST'])

        validator.validate(doc)
