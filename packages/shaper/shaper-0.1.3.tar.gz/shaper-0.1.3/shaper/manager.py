#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""shaper manager - manage library"""

import fnmatch
import os

from . import libs


def walk_on_path(path):
    """Recursively find files with pattern."""

    for root, _, files in os.walk(path):
        for pattern in libs.PARSERS_MAPPING:
            for filename in fnmatch.filter(files, '*{ext}'.format(ext=pattern)):
                yield os.path.join(root, filename)


def create_folders(path_to_folder):
    """Recursively creating folders."""

    try:
        os.makedirs(path_to_folder)
    except OSError:
        if not os.path.isdir(path_to_folder):
            raise EOFError


def read_properties(_dir):
    """Interface for reading properties recursively."""

    result = {
        filename: libs.parser.read(filename) for filename in walk_on_path(_dir)
    }

    return {key: value for key, value in result.items() if value}


def write_properties(datastructure, path):
    """Interface for writing properties recursively."""

    for filename, properties in datastructure.items():
        directories = os.path.join(
            path,
            os.path.dirname(filename)
        )
        create_folders(directories)

        property_file = os.path.basename(filename)
        libs.parser.write(
            properties,
            os.path.join(directories, property_file),
        )


def forward_path_parser(_input):
    """Parsing plain dict to nested."""

    def create_keys_recursively(key, current_tree):
        """Update current tree by key(s)."""

        if key not in current_tree:
            last = keys.pop()
            # pylint: disable=undefined-loop-variable
            # this value defined in the shared outer-function scope
            dict_update = {last: value}

            for _key in reversed(keys):
                dict_update = {_key: dict_update}

            current_tree.update(dict_update)
        else:
            keys.pop(0)  # drop the first item that already in the tree, try next
            create_keys_recursively(keys[0], current_tree[key])

    output = {}
    for key, value in _input.items():
        keys = key.split('/')

        create_keys_recursively(keys[0], output)

    return output


def backward_path_parser(_input):
    """Make nested structure plain."""

    def path_builder(current_tree, key=''):
        """Join all the keys from tree into right path."""

        for _key, _value in current_tree.items():
            _key = key + '/' + _key if key else _key
            if '.' in _key:
                output.update({_key: _value})
            else:
                path_builder(_value, _key)

    output = {}
    path_builder(_input)

    return output
