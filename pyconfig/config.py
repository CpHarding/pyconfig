#! python3
import os
import configparser

import re


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
        self._update_count = 0
        self._ignore_update_count = False
        self.update()
        self._ignore_update_count = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.write()

    def __repr__(self):
        return 'Config({})'.format(self.filepath)

    def update(self):
        """ Updates the internal copy with the contents on disk"""
        self._update_count += 1
        try:
            self.contents = self.config.read(self.filepath)
        except configparser.MissingSectionHeaderError as err:
            raise err
        except configparser.ParsingError as err:
            if not self._ignore_update_count:
                # Remove lines which have errors in them
                line = re.findall(r' ([0-9]+)\]:', err.message)[0]
                line = int(line) - 1
                with open(self.filepath) as f:
                    lines = f.readlines()
                lines[line] = f'# ERROR IN THIS LINE: {lines[line]}'
                with open(self.filepath, 'w') as f:
                    f.writelines(lines)
                # Excessive recursion prevention
                if self._update_count < 1000:
                    self.update()
                else:
                    raise RecursionError('Too many errors in config file')

    def __getattr__(self, item):
        try:
            return self.config[self.default_section][item]
        except KeyError:
            raise AttributeError(f'{item} not found in {self}')

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
