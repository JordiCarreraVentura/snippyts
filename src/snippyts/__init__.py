from doctest import testmod
from itertools import chain
from typing import Any, List


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



if __name__ == '__main__':
    testmod()