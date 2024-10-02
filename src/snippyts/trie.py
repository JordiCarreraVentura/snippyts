
from collections import defaultdict as deft

from copy import deepcopy as cp

class FailedToApproximateFuzzySearchError(RuntimeError):
    pass


META = '#^%s$#'


class Trie:

    def __init__(self):
        self._tree = dict([])
        self._data = dict([])
        self.match = None

    def __iadd__(self, W):
        for w in W:
            self.add(w)
        return self

    def __contains__(self, w):
        return self.search(w, ratio=1.0)

    def add(self, _w):
        w = _w.lower()
        parts = list(w)
        tree = self._tree
        while parts:
            part = parts.pop(0)
            if part not in tree:
                tree[part] = dict([])
            tree = tree[part]
        tree[META % w] = True
        self._data[META % w] = _w

    def search(self, w, ratio=1.0, min_size=0):
        self.match = None
        self.approximation = None
        return self.__lookup(
            w, self._tree, [], list(w.lower()), ratio, min_size
        )

    def __lookup(self, w, tree, history, remainder, ratio, min_size):
        part = remainder.pop(0)
        if part in tree:
            if not remainder and META % w.lower() in tree[part]:
                self.match = self._data[META % w.lower()]
                return True
            elif remainder:
                return self.__lookup(
                    w, tree[part], history + [part], remainder, ratio, min_size
                )
            else:
                return self.approximates(
                    w, tree, history, remainder, ratio, min_size
                )
        else:
            return self.approximates(
                w, tree, history, remainder, ratio, min_size
            )
        return False

    def approximated(self, tree):
        has_aproximation = False
        trees = [tree]
        while True:
            _trees = []
            for _tree in trees:
                for _key, val in _tree.items():
                    if val == True:
                        key = _key.lstrip('#^')
                        key = key.rstrip('$#')
                        self.match = self._data[_key]
                        has_aproximation = True
                        break
                    else:
                        _trees.append(val)
                if has_aproximation:
                    break
            if has_aproximation:
                break
            trees = _trees
            if not trees:
                break
        if not has_aproximation:
            raise FailedToApproximateFuzzySearchError(tree)
#
    def approximates(self, w, tree, history, remainder, ratio, min_size):

        if ratio == 1.0:
            return False
        if not (history and remainder):
            return False
        elif len(history) < min_size:
            return False

        self.approximated(tree)
        if (
            1 - (len(remainder) / float(len(w))) >= ratio
            #and (len(history) / float(len(w))) >= ratio
            and (len(history) / float(len(self.match))) >= ratio
        ):
            return True
        return False

    def __getitem__(self, w):
        return self._data[w]

    def __len__(self):
        return len(self._data)


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