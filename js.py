import os
import re

from subprocess import call
from glsl import compress_glsl
from os import path

def inline_modules(source, directory, imported = []):
    """ Inline modules

    :param source: The source Javascript string
    :param directory: The root directory
    :param imported: All files inlined so far
    :return: The source with all modules recursively inlined
    """

    def include(match):
        head, tail = path.split(match[1])

        if tail in imported:
            return ""

        imported.append(tail)

        contents = ""

        with open(path.join(directory, head, tail), 'r') as file:
            contents = inline_modules(file.read(), path.join(directory, head), imported)

            file.close()

        return contents

    return re.sub('import {.*} from "(.*)";', lambda match: include(match), source.replace("export ", ""))


def compress_js(directory, source, css_variables, advanced_cc):
    """ Compress Javascript content

    :param directory: The root directory
    :param source: The source Javascript string
    :param css_variables: A CSS variables object to shorten css variable names
    :param advanced_cc: True if advanced optimizations should be used
    :return: The compressed source
    """

    with open('tmp-in', 'w') as file:
        file.write(inline_modules(source, directory))
        file.close()

    # TODO: include all externs in cc folder

    extern_dir = os.path.join(os.path.dirname(__file__), 'cc')

    call('npx google-closure-compiler\
        --compilation_level=' + ('ADVANCED_OPTIMIZATIONS' if advanced_cc else 'SIMPLE_OPTIMIZATIONS') + '\
        --language_out=ECMASCRIPT5\
        --warning_level=QUIET\
        --js=tmp-in ' + os.path.join(extern_dir, 'w3c_audio.js') + '\
        --js_output_file=tmp-out', shell=True)
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

    return re.sub(r'"(--[a-zA-Z-]*)"', found, contents)
