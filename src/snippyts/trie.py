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
        Constructor for an instance of a trie that allows for very fast exact
        string look-up (methods `call`, `contains`) as well as fast substring
        search by prefix (method `search`).

        Terms can be added to the trie either with incremental sum
        (`trie += list[str]`) or using the method `add`. Refer to the examples
        for details.

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
        ...    "orwelliano", "oráculo", "oración",
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

        >>> trie = Trie(case_sensitive=True)
        >>> trie += [
        ...    "orca", "Orco", "orco", "oro", "Orwell",
        ...    "orwelliano", "oráculo", "oración"
        ... ]
        >>> assert trie.search('Or') == ['Orco', 'Orwell']
        >>> assert trie('ora') == []
        >>> assert trie.search("ora") == ['oraculo', 'oracion']
        >>> assert trie('Orco') == ['Orco']
        >>> assert trie.search("orco") == ['orco']

        >>> trie = Trie(decode_ascii=False)
        >>> trie += [
        ...    "orca", "Orco", "orco", "oro",
        ...    "orwelliano", "oráculo", "oración",
        ... ]
        >>> assert trie('ora') == []
        >>> assert trie.search("ora") == ['oración']
        >>> assert trie("oracion") == []
        >>> assert trie.search("oracion") == []
        >>> assert trie("oración") == ['oración']
        >>> assert trie.search("oració") == ['oración']

        """
        self.case_sensitive = case_sensitive
        self.decode_ascii = decode_ascii
        self._tree = dict([])

    def __iadd__(self, words: List[str]) -> Any:
        """
        Parameters
        ----------
        word: List[str]
            A wrapper around the `add` method that supports
            iterable objects as input, for convenience.

        Returns
        -------
        snippyts.Trie
            The same object the method has been called on.

        """
        for word in words:
            self.add(word)
        return self

    def __preprocess_word(self, word: str) -> str:
        word = word.lower() if not self.case_sensitive else word
        if self.decode_ascii:
            word = unidecode(word)
        return word

    def add(self, word: str) -> None:
        """
        Parameters
        ----------
        word: str
            New term to be added to the trie.

        Returns
        -------
        Nothing.

        """
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

    def __contains__(self, word: str) -> bool:
        """
        Parameters
        ----------
        word: str
            A string of arbitrary length to look up on the trie.

        Returns
        -------
        bool
            True if the trie contains the value denoted by the input
            argument, and False otherwise.

            A full match is required (over all the characters in the input
            string), otherwise no matches are returned and none are assumed
            to exist.

            Note that this method is a wrapper around the class's call.

            To get matches for partial strings, use method `search` instead.
        """
        return True if self(w) else False

    def search(self, word: str) -> List[str]:
        """
        Parameters
        ----------
        word: str
            A string of arbitrary length to look up on the trie.

            The value can denote both a partial string or a full string.
            Regardless, method `search` will return all matches of that
            string, including longer terms the matching string is a substring
            of. To force full matches, call the class itself, or invoke its
            `contains` method.

        Returns
        -------
        List[str]
            A list with all the strings matching the input substring provided
            as the value of argument `word`.

        """
        word = self.__preprocess_word(word)
        candidates = self.__lookup(
            word, self._tree, [], list(word), []
        )
        return candidates

    def __call__(self, word: str) -> List[str]:
        """
        Parameters
        ----------
        word: str
            A string of arbitrary length to look up on the trie.

        Returns
        -------
        bool
            True if the trie contains the value denoted by the input
            argument, and False otherwise.

            A full match is required (over all the characters in the input
            string), otherwise no matches are returned and none are assumed
            to exist.

            To get matches for partial strings, use method `search` instead.
        """
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



def test_speed():

    import math
    import random
    import time

    letters = list('qwertyuiopasdfghjklzxcvbnm')

    def random_word():
        letter_indexes = [
            random.randrange(len(letters))
            for _ in range(random.randrange(3, 15))
        ]
        return ''.join([letters[i] for i in letter_indexes])

    vocab = [random_word() for _ in range(10000)]
    test_set = [word for word in vocab]
    for pool_oversample, times_oversampled in [
        (random.sample(vocab, 100), 1000),
        (random.sample(vocab, 1000), 100),
        (random.sample(vocab, 10000), 10)
    ]:
        for word in pool_oversample:
            test_set += [word] * times_oversampled

    n_eval = 10000
    trie = Trie()
    trie += test_set
    start = time.time()
    trie.add("Arda")
    for w in random.sample(vocab + ["Ard"], n_eval):
        results = trie.search(w)
        if w in "Arda":
            assert True
    runtime = time.time() - start
    throughput_second = n_eval * (1 / runtime)

    assert runtime < 0.05
    assert round(math.log(throughput_second, 10)) >= 5


def test():
    testmod()
    test_speed()


if __name__ == '__main__':
    test()