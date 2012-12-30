# This file is part of beets.
# Copyright 2012, Adrian Sampson.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

"""Conversion from legacy (pre-1.1) configuration to Confit/YAML
configuration.
"""
import os
import ConfigParser
import codecs
import yaml
import logging

from beets import util
from beets import ui
from beets.util import confit

CONFIG_PATH_VAR = 'BEETSCONFIG'
DEFAULT_CONFIG_FILENAME_UNIX = '.beetsconfig'
DEFAULT_CONFIG_FILENAME_WINDOWS = 'beetsconfig.ini'
DEFAULT_LIBRARY_FILENAME_UNIX = '.beetsmusic.blb'
DEFAULT_LIBRARY_FILENAME_WINDOWS = 'beetsmusic.blb'
WINDOWS_BASEDIR = os.environ.get('APPDATA') or '~'

log = logging.getLogger('beets')

def default_paths():
    """Produces the appropriate default config and library database
    paths for the current system. On Unix, this is always in ~. On
    Windows, tries ~ first and then $APPDATA for the config and library
    files (for backwards compatibility).
    """
    windows = os.path.__name__ == 'ntpath'
    if windows:
        windata = os.environ.get('APPDATA') or '~'

    # Shorthand for joining paths.
    def exp(*vals):
        return os.path.expanduser(os.path.join(*vals))

    config = exp('~', DEFAULT_CONFIG_FILENAME_UNIX)
    if windows and not os.path.exists(config):
        config = exp(windata, DEFAULT_CONFIG_FILENAME_WINDOWS)

    libpath = exp('~', DEFAULT_LIBRARY_FILENAME_UNIX)
    if windows and not os.path.exists(libpath):
        libpath = exp(windata, DEFAULT_LIBRARY_FILENAME_WINDOWS)

    return config, libpath

def get_config():
    """Using the same logic as beets 1.0, locate and read the
    .beetsconfig file. Return a ConfigParser instance or None if no
    config is found.
    """
    default_config, default_libpath = default_paths()
    if CONFIG_PATH_VAR in os.environ:
        configpath = os.path.expanduser(os.environ[CONFIG_PATH_VAR])
    else:
        configpath = default_config

    config = ConfigParser.SafeConfigParser()
    if os.path.exists(util.syspath(configpath)):
        with codecs.open(configpath, 'r', encoding='utf-8') as f:
            config.readfp(f)
        return config, configpath
    else:
        return None, configpath

def flatten_config(config):
    """Given a ConfigParser, flatten the values into a dict-of-dicts
    representation where each section gets its own dictionary of values.
    """
    out = confit.OrderedDict()
    for section in config.sections():
        sec_dict = out[section] = confit.OrderedDict()
        for option in config.options(section):
            sec_dict[option] = config.get(section, option)
    return out

def transform_value(value):
    """Given a string read as the value of a config option, return a
    massaged version of that value (possibly with a different type).
    """
    # Booleans.
    if value.lower() in ('false', 'no', 'off'):
        return False
    elif value.lower() in ('true', 'yes', 'on'):
        return True

    # Integers.
    try:
        return int(value)
    except ValueError:
        pass

    # Floats.
    try:
        return float(value)
    except ValueError:
        pass
    
    return value

def transform_data(data):
    """Given a dict-of-dicts representation of legacy config data, tweak
    the data into a new form. This new form is suitable for dumping as
    YAML.
    """
    out = confit.OrderedDict()

    for section, pairs in data.items():
        if section == 'beets':
            # The "main" section. In the new config system, these values
            # are in the "root": no section at all.
            for key, value in pairs.items():
                out[key] = transform_value(value)

        else:
            # Other sections (plugins, etc).
            sec_out = out[section] = confit.OrderedDict()
            for key, value in pairs.items():
                sec_out[key] = transform_value(value)

    return out

class Dumper(yaml.SafeDumper):
    """A PyYAML Dumper that represents OrderedDicts as ordinary mappings
    (in order, of course).
    """
    # From http://pyyaml.org/attachment/ticket/161/use_ordered_dict.py
    def represent_mapping(self, tag, mapping, flow_style=None):
        value = []
        node = yaml.MappingNode(tag, value, flow_style=flow_style)
        if self.alias_key is not None:
            self.represented_objects[self.alias_key] = node
        best_style = True
        if hasattr(mapping, 'items'):
            mapping = list(mapping.items())
        for item_key, item_value in mapping:
            node_key = self.represent_data(item_key)
            node_value = self.represent_data(item_value)
            if not (isinstance(node_key, yaml.ScalarNode) and \
                    not node_key.style):
                best_style = False
            if not (isinstance(node_value, yaml.ScalarNode) and \
                    not node_value.style):
                best_style = False
            value.append((node_key, node_value))
        if flow_style is None:
            if self.default_flow_style is not None:
                node.flow_style = self.default_flow_style
            else:
                node.flow_style = best_style
        return node
Dumper.add_representer(confit.OrderedDict, Dumper.represent_dict)

def migrate_config():
    config, configpath = get_config()
    if config:
        log.info(u'migrating config file {0}'.format(
            util.displayable_path(configpath)
        ))
        data = transform_data(flatten_config(config))
        print(yaml.dump(data,
                        Dumper=Dumper,
                        default_flow_style=False,
                        indent=4,
                        width=1000))
    else:
        log.info(u'no config file found at {0}'.format(
            util.displayable_path(configpath)
        ))

migrate_cmd = ui.Subcommand('migrate', help='convert legacy config')
def migrate_func(lib, opts, args):
    migrate_config()
migrate_cmd.func = migrate_func
