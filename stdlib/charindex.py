"""
``build_index`` builds an inverted index mapping words to sets of Unicode
characters which contain that word in their names. For example::

    >>> index = build_index(32, 128)
    >>> sorted(index['SIGN'])
    ['#', '$', '%', '+', '<', '=', '>']
    >>> sorted(str(c) for c in index['DIGIT'])
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> index['DIGIT'] & index['EIGHT']
    {'8'}
    >>> search(index, 'digit')
    ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    >>> search(index, 'eight digit')
    ['8']
    >>> search(index, 'a letter')
    ['A', 'a']
    >>> search(index, 'a letter capital')
    ['A']
    >>> search(index, 'borogove')
    []

"""

import sys
import unicodedata
import collections

STOP_CODE = sys.maxunicode + 1


def tokenize(text: str):
    """return iterator of uppercased words"""
    for word in text.upper().replace('-', ' ').split():
        yield word


def build_index(start=32, end=STOP_CODE):
    index = collections.defaultdict(set)
    for char in (chr(i) for i in range(start, end)):
        name = unicodedata.name(char, '')
        if name:
            for word in tokenize(name):
                index[word].add(char)
    return index


def search(index, query):
    words = list(tokenize(query))
    if words:
        first = index[words[0]]
        result = first.intersection(*(index[w] for w in words[1:]))
        return sorted(result)
    else:
        return []
