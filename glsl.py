import re

from shortNames import ShortNames


def __substitute_macros(source):
    """ Substitute macro definitions

    :param source: The source GLSL string
    :return: The source with macro definitions inlined
    """

    macros = {}

    def found_definition(match):
        nonlocal macros

        macros[match[1]] = match[2]

        return ''

    def found_occurrence(match):
        nonlocal macros

        if match[1] in macros:
            return match[0].replace(match[1], macros[match[1]])

        return match[0]

    # Find all macros and their values and delete them
    source = re.sub(re.compile(r'#define ([A-Z_]+) ([^\\n]+)'), found_definition, source)

    # Inline macros
    return re.sub(re.compile(r'[^a-zA-Z_\d]([A-Z_][A-Z_\d]*)'), found_occurrence, source)


def __strip_readability(source):
    """ Strip readability characters from the source

    :param source: The source GLSL string
    :return: The GLSL string without readability characters
    """

    # Remove all redundant newlines
    source = re.sub(re.compile(r'(?<!#version 100)\\n'), ' ', source)

    # Remove all non essential tabs and spaces
    return re.sub(re.compile(r'(?<!\s)((?<=[\W])\s+|\s+(?=[\W]))'), '', source)


def __shorten_floats(source):
    """ Use short float notation whenever possible

    :param source: The source GLSL string
    :return: The GLSL string with short float notation applied
    """

    # Strip redundant leading digits
    source = re.sub(re.compile(r'(?<=[^\d.])0(?=\.)'), '', source)

    # Strip redundant trailing digits
    return re.sub(re.compile(r'(?<=\d\.)0(?=\D)'), '', source)


def compress_glsl(source):
    """ Compress GLSL contents

    :param source: The source GLSL string
    :return: The compressed source
    """

    return __shorten_floats(
        __strip_readability(
            __substitute_macros(
                source)))
