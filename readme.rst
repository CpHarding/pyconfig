PyConfig - A Simple Wrapper around configparser.
===============================================
Written for Python 3.6, but should work with 3.3+

Usage:
=====

Basic Usage
    >>> c = Config()
    >>> c.get('test')
    False
    >>> c.add('test', 'Hello World')
    >>> c.get('test')
    'Hello World'

Using Custom filename
    >>> c = Config(filename='SomeName.ini')

Using Custom Path
    >>> c = Config(path='SomePath')

Write changes to file immediately
    >>> c = Config(write_on_change=True)

Change default section name
    >>> c = Config(default_section='SomeSectionName')

Using Default Values
    >>> c.get('test1')
    False
    >>> c.get('test1', default='Foo')
    'Foo'
    # But this doesn't add it
    >>> c.get('test1')
    False
    # Unless the add flag is used!
    >>> c.get('test1', default='Foo', add=True)
    'Foo'
    >>> c.get('test1')
    'Foo'
Items can be accessed from class attributes (if they are in the default section)
    >>> c.test1
    'Foo'

Get from a non-default section
    >>> c.get('test2', section='Bar')

Adding Values
    >>> c.add('Name', 'Value')
    >>> c.add('Name', 'Value', section='Section2')
    
Write Config to file
    >>> c.write()

Dump Config to a string
    >>> c.dump()

Even use as a context manager, contents is written on __exit__
    >>> with Config() as s:
    >>>     c.get('Test')

Update the internal copy with the file
    >>> c.update()

On inital reading of the file - if any unparseable lines are found they are auto-commented out.
However comments are removed on writing the file, due to the background libary (for now!)