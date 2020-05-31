import sys
import re
import pathlib

from os import path


class Document:
    PATTERN_JS_FILES = '(?<=<script src=\")[^\"]*'

    """
    A document to squish

    :param source: The source HTML file
    """
    def __init__(self, source):
        self.__root = str(pathlib.Path(source).parent.absolute())

        with open(source, 'r') as file:
            self.__source = file.read()

    """
    Process a document
    
    :param target: The target output HTML file
    """
    def process(self, target):
        self.__collect_js()

    """
    Concatenate all referenced javascript includes from the source file
    """
    def __collect_js(self):
        combined = ''

        for script in re.findall(self.PATTERN_JS_FILES, self.__source):
            with open(self.__root + '\\' + script, 'r') as js:
                combined += js.read()

        return combined


if __name__ == "__main__":
    args = dict(zip(['call', 'source', 'target'], sys.argv))

    if 'source' not in args or not path.exists(args['source']):
        print('Please provide a valid input source')
    else:
        if 'target' not in args:
            print('Please provide a valid output target')
        else:
            Document(args['source']).process(args['target'])
