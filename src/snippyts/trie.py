from collections import defaultdict as deft
from doctest import testmod
from typing import Any, Dict, List, Union

from unidecode import unidecode


class Trie:

    def __init__(
        self,
        case_sensitive: bool = False,
        decode_ascii: bool = True
    ) -> None:
        """
        Constructor for an instance of a Trie.

        Parameters
        ----------
        case_sensitive: bool
            If set to true, look-up on the Trie is case-sensitive. It is
            insensitive otherwise (and by default).

        decode_ascii: bool
            If set to false, non-ASCII strings are first decoded into ASCII strings
            are then added to the Trie. The Trie will thus return matches for the
            ASCII strings, not the original ones. No mapping between both encodings
            is kept inside the Trie and it should be implemented if needed.


        Examples
        --------
        >>> trie = Trie()
        >>> trie += [
        ...    "orca", "Orco", "orco", "oro",
        ...    "orwelliano", "oráculo", "oración"
        ... ]

        >>> assert trie('a') == []
        >>> assert trie.search("a") == []

        >>> assert trie('or') == []
        >>> assert trie.search("or") == [
        ...   'orca', 'orco', 'oro',
        ...   'orwelliano', 'oraculo', 'oracion'
        ... ]

        >>> assert trie('ora') == []
        >>> assert trie.search("ora") == ['oraculo', 'oracion']

        >>> assert trie('orco') == ['orco']
        >>> assert trie.search("orco") == ['orco']

        """
        self.case_sensitive = case_sensitive
        self.decode_ascii = decode_ascii
        self._tree = dict([])

    def __iadd__(self, words: List[str]) -> Any:
        for word in words:
            self.add(word)
        return self

    def __preprocess_word(self, word: str) -> str:
        word = word.lower() if not self.case_sensitive else word
        if self.decode_ascii:
            word = unidecode(word)
        return word

    def add(self, word: str) -> None:
        word = self.__preprocess_word(word)
        parts = list(word)
        tree = self._tree
        while parts:
            part = parts.pop(0)
            if part not in tree:
                tree[part] = dict([])
            tree = tree[part]
            if not parts:
                tree["#"] = True

    def __contains__(self, word: str) -> List[str]:
        return self(w)

    def search(self, word: str) -> List[str]:
        word = self.__preprocess_word(word)
        candidates = self.__lookup(
            word, self._tree, [], list(word), []
        )
        return candidates

    def __call__(self, word: str) -> List[str]:
        candidates = self.search(word)
        return [candidate for candidate in candidates if candidate == word]

    def __lookup(
        self,
        word: str,
        tree: Dict[str, Union[str, Dict]],
        history: List[str],
        remainder: List[str],
        results: List[str],
    ) -> List[str]:
        part = remainder.pop(0)
        if part not in tree:
            return results
        else:
            tree = tree[part]
            if remainder:
                return self.__lookup(
                    word, tree, history + [part], remainder, results
                )
            else:
                return results + self.__pull_all_children(history + [part], tree)

    def __pull_all_children(
        self,
        history: List[str],
        tree: List[str]
    ) -> List[str]:
        _children = []
        for key, val in tree.items():
            if key == "#":
                _children.append("".join(history))
                continue
            _child = [ch for ch in history] + [key]
            if val.keys():
                _children += self.__pull_all_children(_child, val)
            else:
                _children.append(_child)
        return _children



def test():

#     trie = Trie()
#     trie.add('Orco')
#     print(trie.search('a'))
#     exit()


    import json
    import random
    from tqdm import tqdm

    letters = list('qwertyuiopasdfghjklzxcvbnm')

    def random_word():
        letter_indexes = [
            random.randrange(len(letters))
            for _ in range(random.randrange(3, 15))
        ]
        return ''.join([letters[i] for i in letter_indexes])


    trie = Trie()
    trie.add('book')
    print(trie._tree)

    print('Test "book" given "book", syntax `in` --- %s' % ('book' in trie))
    print('Test "booklet" given "book", syntax `in` --- %s' % ('booklet' in trie))
    print('Test "bag" given "book", syntax `in` --- %s' % ('bag' in trie))

    print('Test "book" given "book", syntax `search` --- %s' % trie.search('book'))
    print('Test "booklet" given "book", syntax `search`  --- %s' % trie.search('booklet'))
    print('Test "bag" given "book", syntax `search`  --- %s' % trie.search('bag'))
    print('Test "booklet" given "book", syntax `search`, ratio=0.3  --- %s' % trie.search('booklet', ratio=0.3))
    print('Test "booklet" given "book", syntax `search`, ratio=0.5  --- %s' % trie.search('booklet', ratio=0.5))
    print('Test "booklet" given "book", syntax `search`, ratio=0.7  --- %s' % trie.search('booklet', ratio=0.75))

#     exit()
    n_test_words = 10000
    tests = set([])
    true_negatives = set([])
    while len(tests) < n_test_words:
        w = random_word()
        if w in tests:
            continue
        if len(tests) < n_test_words - 10:
            trie.add(w)
        else:
            true_negatives.add(w)
        tests.add(w)
    print('%d tests' % len(tests))
    print('%d elements in Trie' % len(trie))

    tp, tn = 0, 0
    for test in tests:
        try:
            if test in true_negatives:
                assert test not in trie
                tn += 1
                print(test, 'True negative (%d)' % tn)

            elif test in tests:
                assert test in trie
                tp += 1
                print(test, 'True positive (%d)' % tp)

            else:
                raise AssertionError(test)

        except Exception:
            print(json.dumps(sorted(trie._data), indent=4))
            print(test)
            raise AssertionError(test)



if __name__ == '__main__':
    test()