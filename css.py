import os
import re

from subprocess import call


def __capitalize_hexadecimals(source):
    """ Capitalize all hexadecimal strings

    :param source: The source CSS string
    :return: The CSS string with all hexadecimal values capitalized
    """

    def found(match):
        return match[0].replace(match[1], match[1].lower())

    return re.sub(r'#([\dabcdefABCDEF]{8}|[\dabcdefABCDEF]{6}|[\dabcdefABCDEF]{3})', found, source)


def __group_variables(source):
    """
    Group all variables together at the start of the CSS contents

    :param source: The source CSS string
    :return: The CSS string with all variables grouped at the start of the string
    """

    variables = ""

    def found(match):
        nonlocal variables

        variables += match[1]

        return ""

    stripped = re.sub(r':root ?{([^}]*)}', found, source)

    return ":root{" + variables + "}" + stripped


def compress_css(source, css_variables):
    """ Compress CSS content

    :param source: The source CSS string
    :param css_variables: A CSS variables object to register variable names
    :return: The compressed source
    """

    with open('tmp-in', 'w') as file:
        file.write(__group_variables(source))
        file.close()

    call('npx cleancss -o tmp-out tmp-in', shell=True)
    os.remove('tmp-in')

    with open('tmp-out', 'r') as file:
        contents = file.read()
        file.close()

    os.remove('tmp-out')

    return __capitalize_hexadecimals(contents)
