from collections import OrderedDict
import json
from pickle import (
    dump as pdump,
    load as pload
)

from doctest import testmod
from itertools import chain
from typing import Any, Dict, List

from .trie import (
    test as test_trie,
    Trie
)
from .vocabulary_tools import (
    ExactStringMatcher,
    FuzzyStringMatcher,
    NestedObjectsNotSupportedError,
    StringMatcher,
)


def batched(iterable: List[Any], batch_size: int) -> List[List[Any]]:
    """
    Partitions an input collection `iterable` into chunks of size `batch_size`.
    The number of chunks is unknown at the time of calling is determined by
    the length of `iterable`.

    Parameters
    ----------
    iterable:   List[Any]

    batch_size: int

    Returns
    -------
    List[List[Any]]

    Examples
    --------
    >>> iterable = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> chunks = batched(iterable, batch_size=2)
    >>> assert len(chunks) == 4
    >>> assert chunks[0] == [1, 2]
    >>> assert chunks[-1] == [7, 8]

    >>> iterable = [1, 2, 3, 4, 5, 6, 7, 8]
    >>> chunks = batched(iterable, batch_size=12)
    >>> assert len(chunks) == 1
    >>> assert chunks[0] == iterable

    >>> iterable = [1, 2, 3]
    >>> chunks = batched(iterable, batch_size=2)
    >>> assert chunks == [
    ...    [1, 2],
    ...    [3]
    ... ]

    """
    idxs = list(range(len(iterable)))
    ii = [i for i in idxs[::batch_size]]
    return [iterable[i:i + batch_size] for i in ii]


def flatten_loop(lists):
    flattened = []
    for l in lists:
        flattened.extend(l)
    return flattened


def flatten_func(lists):
    return list(chain(*lists))


def flatten(lists: List[List[Any]]) -> List[Any]:
    """
    Given a collection of lists, concatenates all elements into a single list.

    More formally, given a collection holding `n` iterables with `m` elements
    each, this function will return a single list holding all `n * m` elements.

    Parameters
    ----------
    List[List[Any]]

    Returns
    -------
    List[Any]

    Examples
    --------
    >>> example = [[1, 2, 3], [1], [2, 4, 6], [3, 6, 9], [7, 13]]
    >>> len_example = sum(len(l) for l in example)

    >>> assert len_example == len(flatten(example))
    >>> assert len_example == len(flatten_func(example))
    >>> assert len_example == len(flatten_loop(example))

    >>> assert flatten(example) == flatten_func(example)

    >>> assert flatten(example) == flatten_loop(example)
    """
    return [e for l in lists for e in l]


def to_txt(string: str, path: str) -> None:
    """
    Function that expects two string parameters as arguments and writes the
    first string as the content of a file at the location denoted by the second
    string (which is assumed to denote a POSIX path).

    Parameters
    ----------
    string: str
        Some text data to write to disk.

    path: str
        The location where the input text data must be stored, as a POSIX path.

    Returns
    -------
    Nothing, writes the value stored in input variable `string` to the disk
    location denoted by `path`.

    Examples
    --------
    >>> import os
    >>> test_path = "./test_path.txt"

    >>> assert not os.path.exists(test_path)
    >>> to_txt("test raw text.", test_path)
    >>> assert os.path.exists(test_path)
    >>> assert os.path.isfile(test_path)
    >>> assert from_txt(test_path) == "test raw text."

    >>> os.remove(test_path)
    """
    with open(path, 'w') as wrt:
        wrt.write(string)


def from_txt(path: str) -> str:
    """
    Function that can be directed to a local raw text file by its POSIX path
    and returns the content of that file as a string.

    Parameters
    ----------
    path: str
        The location where the input text data must be stored, as a POSIX path.

    Returns
    -------
    str: the raw-text content read from the disk location denoted by the
    argument of parameter `path`.

    Examples
    --------
    >>> import os
    >>> test_path = "./test_path.txt"

    >>> assert not os.path.exists(test_path)
    >>> to_txt("test raw text.", test_path)
    >>> assert os.path.exists(test_path)
    >>> assert os.path.isfile(test_path)
    >>> assert from_txt(test_path) == "test raw text."

    >>> os.remove(test_path)
    """
    with open(path, 'r') as rd:
        return rd.read().strip()


def from_json(path: str) -> Dict[Any, Any]:
    """
    Function that can be directed to a local raw text file by its POSIX path
    and returns the content of that file as a Python dictionary.

    Parameters
    ----------
    path: str
        The location where the input text data must be stored, as a POSIX path.

    Returns
    -------
    str: the dictionary content read from the disk location denoted by the
    argument of parameter `path`.

    Examples
    --------
    >>> import os
    >>> path_json = "json_dump.json"
    >>> assert not os.path.exists(path_json)

    >>> data = {1: "one", 2: "two", 3: "three"}
    >>> to_json(data, path_json)
    >>> assert os.path.exists(path_json)

    >>> keys = list(data.keys())
    >>> for key in keys:
    ...    del data[key]
    >>> assert len(data) == 0

    >>> data.update(from_json(path_json))
    >>> assert len(data) == 3
    >>> assert data == OrderedDict({"1": "one", "2": "two", "3": "three"})

    >>> os.remove(path_json)
    """
    with open(path, 'r') as rd:
        data = json.load(rd, object_pairs_hook=OrderedDict)
    return data


def to_json(dict_: Dict[Any, Any], path: str, indentation: int = 4) -> None:
    """
    Function that expects two parameters as arguments, a Python dictionary and
    a string, and writes the former as the content of a file at the location
    denoted by the latter (which is assumed to denote a POSIX path).

    Parameters
    ----------
    dict_: Any
        A Python dictionary (associative array) whose contents we want
        serialized to disk. The contents must be JSON-dumpable, e.g. no keys
        or values in the dictionary should contain binaries. Otherwise,
        consider pickling the object with `to_pickle`.

    path: str
        The location where the input text data must be stored, as a POSIX path.

    indentation: int
        An integer denoting the indentation to use for every level of nested
        dictionaries stored in input object `dict_`. A dictionary consisting
        of a keys and values will be serialized with an indentation equal to
        `indentation x 1` whitespace characters. If any of those values itself
        contains another dictionary, the values of the latter will be
        serialized with an indentation level equal to `indentation x 2`, and
        so on.

    Returns
    -------
    Nothing, writes the value stored in input variable `payload` to the disk
    location denoted by `path`.

    Examples
    --------
    >>> import os
    >>> path_json = "json_dump.json"
    >>> assert not os.path.exists(path_json)

    >>> data = {1: "one", 2: "two", 3: "three"}
    >>> to_json(data, path_json)
    >>> assert os.path.exists(path_json)

    >>> keys = list(data.keys())
    >>> for key in keys:
    ...    del data[key]
    >>> assert len(data) == 0

    >>> data.update(from_json(path_json))
    >>> assert len(data) == 3
    >>> assert data == OrderedDict({"1": "one", "2": "two", "3": "three"})

    >>> os.remove(path_json)
    """
    with open(path, 'w') as wrt:
      json.dump(dict_, wrt, indent=indentation)



def to_pickle(data: Any, path: str) -> None:
    """
    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    >>> import os
    >>> path_pickle = "pickle_file.p"
    >>> assert not os.path.exists(path_pickle)

    >>> data = {1: "one", 2: "two", 3: "three"}
    >>> to_pickle(data, path_pickle)
    >>> assert os.path.exists(path_pickle)

    >>> keys = list(data.keys())
    >>> for key in keys:
    ...    del data[key]
    >>> assert len(data) == 0

    >>> try:
    ...   from_json(path_pickle)
    ... except Exception:
    ...   assert True

    >>> try:
    ...   from_txt(path_pickle)
    ... except Exception:
    ...   assert True

    >>> data.update(from_pickle(path_pickle))
    >>> assert len(data) == 3
    >>> assert data == {1: "one", 2: "two", 3: "three"}

    >>> os.remove(path_pickle)
    """
    with open(path, "wb") as wrt:
        pdump(data, wrt)


def from_pickle(path: str):
    """
    Parameters
    ----------

    Returns
    -------

    Examples
    --------
    >>> import os
    >>> path_pickle = "pickle_file.p"
    >>> assert not os.path.exists(path_pickle)

    >>> data = {1: "one", 2: "two", 3: "three"}
    >>> to_pickle(data, path_pickle)
    >>> assert os.path.exists(path_pickle)

    >>> keys = list(data.keys())
    >>> for key in keys:
    ...    del data[key]
    >>> assert len(data) == 0

    >>> try:
    ...   from_json(path_pickle)
    ... except Exception:
    ...   assert True

    >>> try:
    ...   from_txt(path_pickle)
    ... except Exception:
    ...   assert True

    >>> data.update(from_pickle(path_pickle))
    >>> assert len(data) == 3
    >>> assert data == {1: "one", 2: "two", 3: "three"}

    >>> os.remove(path_pickle)
    """
    with open(path, "rb") as rd:
        data = pload(rd)
    return data




if __name__ == '__main__':
    testmod()
    test_trie()

