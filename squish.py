import sys
import re
import pathlib

from os import path

from css import compress_css
from js import compress_js
from shortNames import ShortNames


class Document:
    """ A document to compress

    :param source: The source HTML file
    """

    def __init__(self, source):
        self.__root = str(pathlib.Path(source).parent.absolute())

        with open(source, 'r') as file:
            self.__source = self.__remove_readability(file.read())

            file.close()

    def process(self, target, flags):
        """ Process a document

        :param target: The target output HTML file
        :param flags: A dictionary of flags
        """

        self.__collect((
            ('script', 'src', 'script'),
            ('link rel="stylesheet"', 'href', 'style')), flags)

        with open(target, 'w') as file:
            file.write(self.__source)
            file.close()

    @staticmethod
    def __compress(contents, tag, css_variables, flags):
        """ Compress the contents of an HTML tag, if possible

        :param contents: A string that will be compressed
        :param tag: The tag in which the code will be placed, determining its type
        :param css_variables: An object containing all CSS variables
        :param flags: A dictionary of flags
        :return: The compressed contents
        """

        if tag == 'script':
            return compress_js(contents, css_variables, '--advanced-cc' in flags)
        elif tag == 'style':
            return compress_css(contents, css_variables)

        return contents

    @staticmethod
    def __make_tag(tag, contents):
        """ Make a tag with contents

        :param tag: The tag name
        :param contents: The tag contents
        :return: A string containing the tag with its contents
        """

        return '<' + tag + '>' + contents + '</' + tag + '>'

    @staticmethod
    def __make_regex_tag(tags):
        """ Make a regex capturing HTML tags

        :param tags: The tags to search for
        :return: The compiled regular expression
        """

        tags = '(' + '|'.join(tags) + ')'

        return re.compile('<' + tags + ' ([^>]*)(?:>(?!</' + tags + '>)|(?:></' + tags + '>))')

    @staticmethod
    def __make_regex_attribute(attribute):
        """ Make a regex capturing HTML attributes

        :param attribute: The attribute name
        :return: The compiled regular expression
        """

        return re.compile(attribute + '="([^"]*)"')

    @staticmethod
    def __remove_readability(source):
        """ Remove all nonfunctional readability symbols from an HTML string

        :return: A compressed HTML string
        """

        return re.sub(' {2}|\t|\n', '', source)

    @staticmethod
    def __extract_attribute(string, attribute):
        """ Extract an HTML attribute from a string

        :param string: The tags of an attribute
        :param attribute: The attribute name
        :return: The attribute contents as a string
        """

        matches = re.findall(Document.__make_regex_attribute(attribute), string)

        if matches:
            return matches[0]

        return None

    def __extract_tags(self, tags, match):
        """ Extract all occurrences of a given array of tags and replace the tags by the result of a given function

        :param tags: The tag names
        :param match: A function to execute on each match which must return the new HTML code to replace the match with
        """

        self.__source = re.sub(self.__make_regex_tag(tags), match, self.__source)

    def __collect(self, tags, flags):
        """ Include source files referenced by tags directly

        :param tags: A tuple of tuples describing the tags and attributes to look for
        :param flags: A dictionary of flags
        """

        combined = {}
        last_match = {}
        last_index = {}
        attribute = {}
        include_tag = {}

        css_variables = {'namer': ShortNames()}

        for tag in tags:
            combined[tag[0]] = ''
            last_match[tag[0]] = None
            last_index[tag[0]] = self.__source.rfind('<' + tag[0])
            attribute[tag[0]] = tag[1]
            include_tag[tag[0]] = tag[2]

        def get_match(match):
            nonlocal combined
            nonlocal last_match
            nonlocal last_index
            nonlocal css_variables

            tag = match[1]
            source = self.__extract_attribute(match[2], attribute[tag])

            if source is None:
                return match[0]

            with open(path.join(self.__root, source), 'r') as file:
                source_contents = file.read()

                file.close()

            if last_match[tag] is not None:
                if last_match[tag].span()[1] == match.span()[0]:
                    combined[tag] += source_contents
                else:
                    last_match[tag] = match
                    script_contents = combined[tag]
                    combined[tag] = source_contents

                    return self.__make_tag(
                        include_tag[tag],
                        self.__compress(script_contents, include_tag[tag], css_variables, flags))
            else:
                combined[tag] = source_contents

            last_match[tag] = match

            if match.span()[0] == last_index[tag]:
                return self.__make_tag(
                    include_tag[tag],
                    self.__compress(combined[tag], include_tag[tag], css_variables, flags))

            return ''

        self.__extract_tags([tag[0] for tag in tags], get_match)


if __name__ == "__main__":
    args = dict(zip(['call', 'source', 'target'], sys.argv))

    if 'source' not in args or not path.exists(args['source']):
        print('Please provide a valid input source')
    else:
        if 'target' not in args:
            print('Please provide a valid output target')
        else:
            Document(args['source']).process(args['target'], sys.argv)
