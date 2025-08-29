import csv
import json
import requests
import yaml
import os
import sys
from collections.abc import Iterable
from collections import namedtuple, OrderedDict
from copy import deepcopy as cp
from doctest import testmod
from itertools import chain
from pickle import (
    dump as pdump,
    load as pload
)
from typing import Any, Callable, Dict, Iterable, List
from urllib.parse import urlparse

from .trie import (
    test as test_trie,
    Trie
)
from .utilities import (
    UnsupportedInputShapeError,
    is_all_numerical_immutable,
    smart_cast_number,
    tryline
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


def to_yaml(
    data: List[Any],
    path: str
) -> None:
    """
    Function that expects a list of serializable objects and a string denoting
    a path, and writes the data to a YAML file at the given path.

    Parameters
    ----------
    data: List[Any]
        A list of YAML-serializable Python objects.

    path: str
        The location where the input data must be stored, as a POSIX path.

    Returns
    -------
    Nothing. Writes the input variable `data` to the disk location denoted by `path`.

    Examples
    --------
    >>> test_path = "./test_path.yaml"
    >>> data = [{"Name": "John", "Age": 30}, {"Name": "Jane", "Age": 25}]

    >>> assert not os.path.exists(test_path)
    >>> to_yaml(data, test_path)
    >>> assert os.path.exists(test_path)
    >>> assert os.path.isfile(test_path)
    >>> assert from_yaml(test_path) == data
    >>> assert data[0]["Name"] == "John"

    >>> os.remove(test_path)
    """
    with open(path, 'w') as wrt:
        yaml.dump(data, wrt, default_flow_style=False)


def from_yaml(path: str) -> List[Any]:
    """
    Function that reads a YAML file from the specified POSIX path and returns the
    deserialized Python list object.

    Parameters
    ----------
    path: str
        The location where the input data is stored, as a POSIX path.

    Returns
    -------
    List[Any]: The content read from the disk location denoted by the `path`.

    Examples
    --------
    >>> test_path = "./test_path.yaml"
    >>> data = [{"Name": "John", "Age": 30}, {"Name": "Jane", "Age": 25}]

    >>> assert not os.path.exists(test_path)
    >>> to_yaml(data, test_path)
    >>> assert os.path.exists(test_path)
    >>> assert os.path.isfile(test_path)
    >>> assert from_yaml(test_path) == data
    >>> assert from_yaml(test_path)[1]["Age"] == 25

    >>> os.remove(test_path)
    """
    with open(path, 'r') as rd:
        return yaml.safe_load(rd)


def is_number(string: str) -> bool:
    """
    Function that checks whether a string can be interpreted as a integer or a float.

    Parameters
    ----------
    string: str
        String to be checked

    Returns
    -------
    bool: Whether the string can be interpreted as a integer or a float (True), or neither (False).

    Doctests:
    >>> is_number('123')
    True
    >>> is_number('12.3')
    True
    >>> is_number('abc')
    False
    >>> is_number('12.3.4')
    True
    """
    if (
        string.isdigit()
        or string.replace('.', '').isdigit()
    ):
        return True
    return False


def read_arg(name: str) -> Any:
    """
    Function that reads command line arguments passed to a python script, then returns
    the corresponding value of the specified argument's name.

    Parameters
    ----------
    name: str
        The name of the argument whose value is to be returned.

    Returns
    -------
    Any: On finding the matching name in the command line arguments, the function 
    behaves in the following manner:
    - If parameter is followed by another parameter (a value starting with '-'), 
      it returns `True` as the argument for the former.
    - If the parameter is not followed by an argument, it returns `True`.
    - If the argument can be converted to `float`, returns it so converted.
    - If the argument can be converted to `int`, returns it so.
    - In all other cases, returns the value as a string.
    - If no matches are found for the specified parameter name, returns `False`.

    Examples
    --------
    >>> import sys
    >>> sys.argv.extend(['--param_1', 'arg_1'])
    >>> sys.argv.extend(['--param_2'])
    >>> sys.argv.extend(['--param_3', '3'])

    >>> read_arg('param_1')
    'arg_1'
    >>> read_arg('param_2')
    True
    >>> read_arg('param_3')
    3

    Missing arguments default to `False`:
    >>> read_arg('param_4')
    False

    Hyphens must not matter:
    >>> read_arg('--param_1')
    'arg_1'
    >>> read_arg('--param_2')
    True
    >>> read_arg('--param_3')
    3
    """
    args = sys.argv
    name = name.strip('-')
    for idx, param in enumerate(args):
        if not param.strip('-') == name:
            continue
        if idx < len(args) - 1:
            arg = args[idx + 1]
            if arg.startswith('-'):
                return True
        else:
            return True
        if not is_number(arg):
            return arg
        return float(arg) if '.' in arg else int(arg)
    else:
        return False


def read_args(tuple_name: str = 'Parameters') -> namedtuple:
    """
    Function that reads all named command line arguments passed to a Python script
    (names are those starting with '-'), then saves their corresponding values into a 
    namedtuple. The argument names are converted into valid attribute names by 
    stripping leading hyphens and replacing non-alpha-numeric characters with underscores.

    Returns
    -------
    named_params: A namedtuple with attributes being all the named command line 
        arguments passed to the script

    Examples
    --------
    >>> import sys
    >>> sys.argv.extend(['--param_6', 'arg_1_2'])
    >>> sys.argv.extend(['--param_7', '--param_8'])
    >>> sys.argv.extend(['--param_5', '55.3'])
    
    >>> params = read_args()
    >>> params.param_6
    'arg_1_2'
    >>> params.param_2
    True
    >>> assert params.param_7 == params.param_8
    >>> params.param_5
    55.3
    """
    param_names = [param.strip('-') for param in sys.argv if param.startswith('-')]
    args = OrderedDict()
    for param in param_names:
        args[param] = read_arg(param)
    
    named_params = namedtuple(tuple_name, list(args.keys()))(*args.values())
    return named_params


def defolder(path: str) -> str:
    """
    Function that takes a path string as an argument. If a folder at that path does not 
    exist yet, it gets created. It then returns the real path of the folder,
    resolving any symbolic links in the path if they exist.

    Parameters
    ----------
    path: str
        The directory path that should be created and resolved

    Returns
    -------
    str
        The canonical path string of the created/resolved directory

    Examples
    --------
    >>> import os
    >>> folder = os.path.join(os.getcwd(), 'test_defolder_folder')
    >>> assert not os.path.exists(folder)
    >>> path = defolder(folder)
    
    >>> assert os.path.exists(path)
    >>> assert os.path.exists(folder)
    >>> assert os.path.basename(path) == os.path.basename(folder)

    >>> os.removedirs(folder)

    >>> assert not os.path.exists(path)
    >>> assert not os.path.exists(folder)
    """
    dirname = os.path.dirname(path)
    filename = os.path.basename(path)
    has_file = False
    if '.' in filename:
        has_file = True
    target = path if not has_file else dirname
    if not os.path.exists(target):
        os.makedirs(target, exist_ok=True)
    if has_file:
        return os.path.realpath(os.path.join(target, filename))
    else:
        return os.path.realpath(target)



if __name__ == '__main__':
    testmod()
    test_trie()

