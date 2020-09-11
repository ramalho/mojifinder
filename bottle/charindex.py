"""
``InvertedIndex`` builds an inverted index mapping each word to a set of
Unicode characters which contain that word in their names.

The arguments to the constructor are the ``first`` and ``last+1`` character
codes to index. In the example below, only the ASCII range was indexed::

    >>> ii = InvertedIndex(32, 128)
    >>> sorted(ii.index['SIGN'])
    ['#', '$', '%', '+', '<', '=', '>']
    >>> sorted(str(c) for c in ii.index['DIGIT'])
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> ii.index['DIGIT'] & ii.index['EIGHT']
    {'8'}
    >>> ii.search('digit')
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> ii.search('eight digit')
    ['8']
    >>> ii.search('a letter')
    ['A', 'a']
    >>> ii.search('a letter capital')
    ['A']
    >>> ii.search('borogove')
    []

"""

import sys
import unicodedata
import collections

STOP_CODE = sys.maxunicode + 1


def tokenize(text):
    """return iterator of uppercased words"""
    for word in text.upper().replace('-', ' ').split():
        yield word


class InvertedIndex:
    def __init__(self, start=32, end=STOP_CODE):
        index = collections.defaultdict(set)
        for char in (chr(i) for i in range(start, end)):
            name = unicodedata.name(char, '')
            if name:
                for word in tokenize(name):
                    index[word].add(char)
        self.index = index

    def search(self, query):
        words = list(tokenize(query))
        if words:
            first = self.index[words[0]]
            result = first.intersection(*(self.index[w] for w in words[1:]))
            return sorted(result)
        else:
            return []
