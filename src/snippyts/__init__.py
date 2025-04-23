import csv
import json
import requests
from collections.abc import Iterable
from collections import OrderedDict
from pickle import (
    dump as pdump,
    load as pload
)
from urllib.parse import urlparse

from doctest import testmod
from itertools import chain
from typing import Any, Callable, Dict, Iterable, List

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


class NotAUrlError(ValueError):
    pass
    
class ConnectionFailedError(RuntimeError):
    pass
    
class HtmlDocumentParseError(RuntimeError):
    pass
    
class UnsupportedInputShapeError(ValueError):
    pass



def is_all_numerical_immutable(iterable):
    """
    Check if all elements in an iterable are immutable numerical types (int, float, complex).

    Parameters
    ----------
        iterable: Iterable[complex | float | int]
          An iterable of elements to check.

    Returns
    -------
        bool:
          True if all elements are instances of immutable numerical types, False otherwise.

    Raises
    ------
        UnsupportedInputShapeError: If the input is not an iterable.

    Examples
    --------
    >>> is_all_numerical_immutable([1, 2.5, 3])
    True
    >>> is_all_numerical_immutable((1+2j, 3.0))
    True
    >>> is_all_numerical_immutable((333.3, 0.0393, 0.1887))
    True
    >>> is_all_numerical_immutable([1, "2", 3])
    False
    >>> is_all_numerical_immutable(["11", "2", "3"])
    False
    >>> is_all_numerical_immutable("123")
    False
    >>> is_all_numerical_immutable(123)
    Traceback (most recent call last):
    ...
    UnsupportedInputShapeError: Input must be an iterable.

    """
    if not isinstance(iterable, Iterable):
        raise UnsupportedInputShapeError("Input must be an iterable.")
    
    immutable_numerics = (int, float, complex)
    
    return all(isinstance(item, immutable_numerics) for item in iterable)


def tryline(_call: Callable, exception: Exception, *args, **kwargs) -> Any:
    """
    Wraps a try-raise block into a single statement. It is intended to
    flatten try-catch
    
    It attempts to call the specified Python-callable object with the provided 
    arguments and keyword arguments.
    
    If the call is successful, it silently returns the output of the call.
    If it fails, it raises an exception of the type provided as the second
    argument.
    
    Parameters
    ----------
    _call: object
        Any Python object that can be called on the specified arguments.
    
    exception: Exception
        The exception that must be raised if the call fails.
    
    *args: List[Any]
        Its standard meaning.
        
    **kwargs: Dict[str, Any]
        Its standard meaning.
    
    Returns
    -------
    object:
        Whichever object is returned by the call to the callable object.
    
    Examples
    --------
    >>> class CustomError(Exception):
    ...   pass

    >>> assert tryline(sum, CustomError, [1, 1]) == 2
    >>> tryline(
    ...   lambda x, y: x + "." + y,
    ...   CustomError,
    ...   'text',
    ...   'and more text'
    ... )
    'text.and more text'
    
    >>> try:
    ...   tryline(sum, CustomError, ['text', 1])
    ... except CustomError:
    ...   assert True
    
    >>> try:
    ...   tryline(lambda x, y: x + "." + y, CustomError, 'text', 1)
    ... except CustomError:
    ...   assert True
    """
    try:
        return _call(*args, **kwargs)
    except Exception:
        raise exception(args)


def is_url(url: str) -> bool:
    """
    Determines whether a given string is a valid URL.
    
    It uses urllib.parse.urlparse, a function that splits a URL into six 
    components: scheme, network location, path, parameters, query, and 
    fragment. 
    
    A string is considered a URL if both the scheme and the network location
    components exist, and the scheme is http or https.
    
    Parameters
    ----------
    url : str
        The string to be checked.
    
    Returns
    -------
    bool
        True if the input string is a valid URL, False otherwise.
    
    Raises
    ------
    NotAUrlError
        If the string is not a URL, it raises a NotAUrlError.
    
    Examples
    --------
    >>> is_url("https://www.google.com")
    True

    >>> try:
    ...   is_url("not a url")
    ... except NotAUrlError:
    ...   assert True
    """
    
    try:
        result = urlparse(url)
        assert result.scheme in ['http', 'https']
        assert all([result.scheme, result.netloc])
        return True
    except Exception:
        raise NotAUrlError()
        return False


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



def to_csv(
    data: List[Iterable[Any]],
    path: str,
    delimiter: str = ","
) -> None:
    """
    Function that expects a list of iterables (representing rows of printable
    objects) and a string denoting a path, and writes the data to a csv file
    at the path.

    Parameters
    ----------
    data: List[List[str]]
        Some tabular data to write to disk.

    path: str
        The location where the input data must be stored, as a POSIX path.

    Returns
    -------
    Nothing, writes the value stored in input variable `data` to the disk
    location denoted by `path`.

    Examples
    --------
    >>> import os
    >>> test_path = "./test_path.csv"
    >>> data = [["Name", "Age"], ["John", "30"], ["Jane", "25"]]

    >>> assert not os.path.exists(test_path)
    >>> to_csv(data, test_path)
    >>> assert os.path.exists(test_path)
    >>> assert os.path.isfile(test_path)
    >>> assert from_csv(test_path) == data
    >>> assert data[0][1] == "Age"

    >>> os.remove(test_path)
    """
    with open(path, 'w', newline='') as wrt:
        writer = csv.writer(wrt, delimiter=delimiter)
        writer.writerows(data)


def from_csv(path: str, delimiter: str = ",") -> List[List[str]]:
    """
    Function that can be directed to a local csv file by its POSIX path
    and returns the content of that file as a list of lists of strings.

    Parameters
    ----------
    path: str
        The location where the input data is stored, as a POSIX path.

    Returns
    -------
    List[List[str]]: the tabular content read from the disk location denoted by the
    argument of parameter `path`.

    Examples
    --------
    >>> import os
    >>> test_path = "./test_path.csv"
    >>> data = [["Name", "Age"], ["John", "30"], ["Jane", "25"]]

    >>> assert not os.path.exists(test_path)
    >>> to_csv(data, test_path)
    >>> assert os.path.exists(test_path)
    >>> assert os.path.isfile(test_path)
    >>> assert from_csv(test_path) == data
    >>> assert data[0][1] == "Age"

    >>> os.remove(test_path)
    """
    with open(path, 'r') as rd:
        reader = csv.reader(rd, delimiter=delimiter)
        return list(reader)


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


def gtml(url: str) -> str:
    """
    Gets the HTML content of the document at the specified location URL. Named `gtml` as a shorthand for "get HTML".
    
    Parameters
    ----------
    url: str
       URL pointing to an HTML document.
    
    Returns
    -------
    str
       The text of the HTML document.
    
    Raises
    ------
    NotaUrlError
       The input is not a URL.

    ConnectionFailedError
        The input URL is correct but it could not be fetched.
       
    HtmlDocumentParseError
        The input URL is correct and it was correctly fetched, but no text
        could be parsed.
    
    Examples
    -------
    
    # Provided input cannot be parsed as a URL:
    >>> try:
    ...   gtml("hts://stackoverflow.com/questions/4075190/"
    ...        "what-is-how-to-use-getattr-in-python")
    ... except NotAUrlError:
    ...   assert True
    
    # Working as intended:
    >>> html = gtml("https://example.com")
    >>> assert len(html) == 1256
    >>> html = ''.join(html.splitlines()).replace('"', "'") 
    >>> assert html == "<!doctype html><html><head>    <title>Example Domain</title>    <meta charset='utf-8' />    <meta http-equiv='Content-type' content='text/html; charset=utf-8' />    <meta name='viewport' content='width=device-width, initial-scale=1' />    <style type='text/css'>    body {        background-color: #f0f0f2;        margin: 0;        padding: 0;        font-family: -apple-system, system-ui, BlinkMacSystemFont, 'Segoe UI', 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;            }    div {        width: 600px;        margin: 5em auto;        padding: 2em;        background-color: #fdfdff;        border-radius: 0.5em;        box-shadow: 2px 3px 7px 2px rgba(0,0,0,0.02);    }    a:link, a:visited {        color: #38488f;        text-decoration: none;    }    @media (max-width: 700px) {        div {            margin: 0 auto;            width: auto;        }    }    </style>    </head><body><div>    <h1>Example Domain</h1>    <p>This domain is for use in illustrative examples in documents. You may use this    domain in literature without prior coordination or asking for permission.</p>    <p><a href='https://www.iana.org/domains/example'>More information...</a></p></div></body></html>"
    """
    tryline(is_url, NotAUrlError, url)
    response = tryline(requests.get, ConnectionFailedError, url)
    response = requests.get(url)
    response.raise_for_status()
    return tryline(getattr, HtmlDocumentParseError, response, "text")


def smart_cast_number(x: float | int) -> float | int:
    """
    Cast a numeric value to an integer if it is numerically whole; otherwise, return as float.

    Parameters
    ----------
        x: float | int
          A numeric value to be cast intelligently.

    Returns
    -------
        float | int:
          The input value cast to an integer if it has no fractional part, otherwise returned as a float.

    Examples
    --------
    >>> smart_cast_number(1)
    1
    >>> smart_cast_number(1.0)
    1
    >>> smart_cast_number(1.333)
    1.333
    """
    if (
        isinstance(x, int)
        or isinstance(x, float) and int(x) == x
    ):
        return int(x)
    return float(x)



if __name__ == '__main__':
    testmod()
    test_trie()

