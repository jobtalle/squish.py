import os
import re

from subprocess import call
from glsl import compress_glsl


def compress_js(source, css_variables):
    """ Compress Javascript content

    :param source: The source Javascript string
    :param css_variables: A CSS variables object to shorten css variable names
    :return: The compressed source
    """

    with open('tmp-in', 'w') as file:
        file.write(source)
        file.close()

    call('npx google-closure-compiler --flagfile=cc.txt --js=tmp-in --js_output_file=tmp-out', shell=True)
    os.remove('tmp-in')

    with open('tmp-out', 'r') as file:
        contents = file.read().replace('\n', '')

        file.close()

    os.remove('tmp-out')

    contents = re.sub('(?!"")#version 100[^"]*(?=")', lambda match: compress_glsl(match[0]), contents)

    def found(match):
        if match[1] in css_variables:
            return match[0].replace(match[1], css_variables[match[1]])

        return match[0]

    return re.sub(r'"(--[a-z|A-Z|-]*)"', found, contents)
