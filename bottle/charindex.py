"""
``Index`` implements an inverted index mapping words to sets of Unicode
characters which contain that word in their names. For example::

    >>> i = InvertedIndex(32, 128)
    >>> sorted(i.index['SIGN'])
    ['#', '$', '%', '+', '<', '=', '>']
    >>> sorted(str(c) for c in i.index['DIGIT'])
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> i.index['DIGIT'] & i.index['EIGHT']
    {'8'}
    >>> i.search('digit')
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> i.search('eight digit')
    ['8']
    >>> i.search('a letter')
    ['A', 'a']
    >>> i.search('a letter capital')
    ['A']
    >>> i.search('borogove')
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
