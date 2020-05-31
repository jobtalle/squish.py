import sys

from os import path


class Document:
    """
    A document to squish

    :param source: The source HTML file
    """
    def __init__(self, source):
        pass

    """
    Process a document
    
    :param target: The target output HTML file
    """
    def process(self, target):
        print(target)


if __name__ == "__main__":
    args = dict(zip(['call', 'source', 'target'], sys.argv))

    if 'source' not in args or not path.exists(args['source']):
        print('Please provide a valid input source')
    else:
        if 'target' not in args:
            print('Please provide a valid output target')
        else:
            Document(args['source']).process(args['target'])
