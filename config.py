#! python3
import os
import configparser


class Config:
    contents = {}
    def __init__(self, filename='config.ini', path='.', write_on_change=False, default_section='default',
                 *args, **kwargs):
        """
        :param filename: (optional) filename to use
        :param path: (optional) path to use
        :param write_on_change: (bool) write on change
        :param default_section: name of the default section to use
        :param args: pass arguments to background ConfigParser
        :param kwargs: pass arguments to background ConfigParser
        """
        self.config = configparser.ConfigParser(*args, **kwargs)
        self.filepath = os.path.join(path, filename)

        self.default_section = default_section
        self.write_on_change = write_on_change
        self.update()
        self.write()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.write()

    def __repr__(self):
        return 'Config({})'.format(self.filepath)

    def update(self):
        """ Updates the internal copy with the contents on disk"""
        self.contents = self.config.read(self.filepath)

    def add(self, option, value, section=None):
        """
        Add an option to the internal copy
        :param option: option name
        :param value: value to use
        :param section: section, if non default
        :return: None
        """
        section = self.default_section if section is None else section
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config[section][option] = str(value)
        if self.write_on_change:
            self.write()

    def get(self, option, section='default', default=None, add=False):
        """
        Get an option from the internal copy
        :param option: option name
        :param section: section to search
        :param default: default to return if not found
        :param add: add the default to the config?
        :return: value, or default.
        """
        section = self.default_section if section is None else section
        if self.config.has_option(section, option):

            value = self.config[section][option]
            return value
        else:
            if add:
                self.add(option, default, section)
                return default
            else:
                return default if default else False

    def write(self):
        """ Write the internal copy to file"""
        if not os.path.isdir(os.path.dirname(self.filepath)):
            os.makedirs(os.path.dirname(self.filepath))
        with open(self.filepath, 'w') as f:
            self.config.write(f)

    def dump(self):
        """ return a string of the internal copy"""
        dump = {}
        for section in self.config.sections():
            dump[section] = dict(self.config.items(section))
        return dump
