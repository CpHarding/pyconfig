#! python3

import unittest

import os

from config import Config


class TestCreation(unittest.TestCase):
    def tearDown(self):
        try:
            os.remove(self.s.filepath)
            # Will only remove if the directory is empty
            os.removedirs(os.path.dirname(self.s.filepath))
        except Exception:
            pass

    def test_defaults(self):
        try:
            self.s = Config()
        except Exception as e:
            self.fail('Got Exception {}'.format(e))
        self.assertTrue(isinstance(self.s, Config))
        self.assertTrue(os.path.isfile(self.s.filepath))

    def test_filename(self):
        try:
            self.s = Config(filename='SomeTestFile.ini')
        except Exception as e:
            self.fail('Got Exception {}'.format(e))
        self.assertTrue(os.path.isfile('SomeTestFile.ini'))

    def test_path(self):
        try:
            self.s = Config(path='SomeTestPath')
        except Exception as e:
            self.fail('Got Exception {}'.format(e))
        self.assertTrue(os.path.isfile(os.path.join('SomeTestPath', 'config.ini')))

    def test_path_filename(self):
        try:
            self.s = Config(path='SomeTestPath', filename='SomeTestFile.ini')
        except Exception as e:
            self.fail('Got Exception {}'.format(e))
        self.assertTrue(os.path.isfile(os.path.join('SomeTestPath', 'SomeTestFile.ini')))

    def test_write_change(self):
        try:
            self.s = Config(write_on_change=True)
        except Exception as e:
            self.fail('Got Exception {}'.format(e))
        with open(self.s.filepath) as f:
            contents = f.readlines()
        self.s.add('Test', 'Value')
        with open(self.s.filepath) as f:
            self.assertNotEqual(contents, f.readlines())

    def test_default_section(self):
        try:
            self.s = Config(default_section='TestSection')
        except Exception as e:
            self.fail('Got Exception {}'.format(e))
        self.s.add('test', 'value')
        self.assertEqual(self.s.config.sections(), ['TestSection'])


class TestGet(unittest.TestCase):
    def setUp(self):
        self.s = Config()
        self.s.add('Option', 'Value')
        self.s.add('Option', 'Value', section='Test')

    def tearDown(self):
        if os.path.isfile(self.s.filepath):
            os.remove(self.s.filepath)

    def test_get_false(self):
        self.assertFalse(self.s.get('ValueNotPresent'))

    def test_get_value(self):
        self.assertEqual(self.s.get('Option'), 'Value')

    def test_get_default_value(self):
        self.assertEqual(self.s.get('Foo', default='Bar'), 'Bar')
        self.assertFalse(self.s.get('Foo'))

    def test_get_default_value_add(self):
        self.assertEqual(self.s.get('Foo', default='Bar', add=True), 'Bar')
        self.assertEqual(self.s.get('Foo'), 'Bar')

    def test_get_section_false(self):
        self.assertFalse(self.s.get('ValueNotPresent', section='Test'))

    def test_get_section_value(self):
        self.assertEqual(self.s.get('Option', section='Test'), 'Value')

    def test_get_section_default_value(self):
        self.assertEqual(self.s.get('Foo', default='Bar', section='Test'), 'Bar')
        self.assertFalse(self.s.get('Foo', section='Test'))

    def test_get_section_default_value_add(self):
        self.assertEqual(self.s.get('Foo', default='Bar', add=True, section='Test'), 'Bar')
        self.assertEqual(self.s.get('Foo', section='Test'), 'Bar')

    def test_get_attr(self):
        try:
            self.s.Option
        except Exception:
            self.assertTrue(False)
        self.assertTrue(True)

    def test_get_missing_attr(self):
        with self.assertRaises(AttributeError):
            self.s.missing_value




class TestAdd(unittest.TestCase):
    def setUp(self):
        self.s = Config()

    def tearDown(self):
        if os.path.isfile(self.s.filepath):
            os.remove(self.s.filepath)

    def test_add(self):
        self.assertFalse(self.s.get('Foo'))
        try:
            self.s.add('Foo', 'Bar')
        except Exception as e:
            self.fail('Got Exception {}'.format(e))
        self.assertEqual(self.s.get('Foo'), 'Bar')

    def test_add_section(self):
        self.assertFalse(self.s.get('Foo', section='Test'))
        try:
            self.s.add('Foo', 'Bar', section='Test')
        except Exception as e:
            self.fail('Got Exception {}'.format(e))
        self.assertEqual(self.s.get('Foo', section='Test'), 'Bar')

if __name__ == '__main__':
    unittest.discover()
