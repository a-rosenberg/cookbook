#!/usr/bin/env python

import logging
import os
import re


def bulk_change(function):
    """Bulk change for markdown

    Uses input function to modify and overwrite markdown recipes
    to allow for bulk changes in styling and automated product
    generation.

    Args:
        function: Function object to manipulate raw markdown text.
    """
    for root, dirs, files in os.walk('recipes'):
        if not root.startswith('./.'):
            for file in files:
                if file.endswith('.md'):
                    path = os.path.join(root, file)
                    with open(path) as fid:
                        data = fid.read()

                    output = function(data)

                    with open(path, 'w') as oid:
                        oid.write(output)


def header_h2_to_h1(data):
    """Changes <h2> main title to <h1>"""
    logging.info('header_h2_to_h1 on %s')
    output = data.replace('h2', 'h1')
    return output


def section_titles_to_h3(data):
    """Changes section markdown from #### to ###"""
    logging.info('header_h2_to_h1 on %s')
    output = data.replace('####', '###')
    return output


def list_ingredients(data):
    """Lists recipe title and ingredients without changes to text"""
    recipe = re.findall("<h1.*>(.+)</h1>", data)
    if recipe:
        ingredients = re.findall("- (.*)", data)
        print recipe[0]
        for ingredient in ingredients:
            print 'ingredient:', ingredient
        print
    return data


if __name__ == '__main__':
    bulk_change(list_ingredients)