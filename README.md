# snippyts

Miscellaneous utility scripts and Python objects for agile development.

1. [Table of objects](#table-of-objects)
2. [Instructions for running tests](#running-tests)


# Table of objects

| No. | Name | Description | Date added | Date reviewed |
| --- | --- | --- | --- | --- |
| 1 | `snippyts.`<br>`__init__.`<br>`batched` | Partitions an input collection `iterable` into chunks of size `batch_size`. The number of chunks is unknown at the time of calling is determined by the length of `iterable`. | September 22nd, 2024 | September 22nd, 2024 |
| 2 | `snippyts.`<br>`__init__.`<br>`flatten` | Given a collection of lists, concatenates all elements into a single list. More formally, given a collection holding `n` iterables with `m` elements each, this function will return a single list holding all `n * m` elements. | September 22nd, 2024 | September 22nd, 2024 |
| 3 | `create_python_`<br>`simple_package.sh` | BASH script to initialize a local Python package as a local git repository with a virtual environment, project files, and standard folder structure. It takes user input into account for parameterization from the command line. | September 22nd, 2024 | September 23rd, 2024 |
| 4 | `snippyts.`<br>`__init__.`<br>`to_txt` | Function that expects two string parameters as arguments and writes the first string as the content of a file at the location denoted by the second string (which is assumed to denote a POSIX path). | September 23rd, 2024 | September 23rd, 2024 |
| 5 | `snippyts.`<br>`__init__.`<br>`from_txt` | Function that can be directed to a local raw text file by its POSIX path and returns the content of that file as a string. | September 23rd, 2024 | September 23rd, 2024 |
| 6 | `snippyts.`<br>`__init__.`<br>`to_json` | Function that expects two parameters as arguments, a Python dictionary and a string, and writes the former as the content of a file at the location denoted by the latter (which is assumed to denote a POSIX path). | September 24th, 2024 | September 24th, 2024 |
| 7 | `snippyts.`<br>`__init__.`<br>`from_json` | Function that can be directed to a local JSON file by its POSIX path and returns the content of that file as a Python dictionary. | September 24th, 2024 | September 24th, 2024 |
| 8 | `snippyts.`<br>`__init__.`<br>`to_pickle` | Function that can be directed to a local raw text file by its POSIX path and returns the content of that file as a Python dictionary. | October 3rd, 2024 | October 3rd, 2024 |
| 9 | `snippyts.`<br>`__init__.`<br>`from_pickle` | Function that can be directed to a local Python-pickle file by its POSIX path and returns a copy of the artifact  persisted in that file. | October 3rd, 2024 | October 3rd, 2024 |
| 10 | `snippyts.trie.Trie` | A class implementing a [trie](https://en.wikipedia.org/wiki/Trie) data structure. | October 3rd, 2024 | October 3rd, 2024 |
| 11 | `snippyts.`<br>`vocabulary_tools.`<br>`ExactStringMatcher` | A wrapper around `flashtext2` providing a unified application interface shared with `FuzzySet`. | October 12th, 2024 | October 26th, 2024 |
| 12 | `snippyts.`<br>`vocabulary_tools.`<br>`FuzzyStringMatcher` | A wrapper around `FuzzySet` providing a unified application interface shared with `flashtext2`. | October 13th, 2024 | October 26th, 2024 |
| 13 | `snippyts.`<br>`__init__.`<br>`to_csv` | Function that expects two parameters as arguments, a list of lists (or, more geneally, an Iterable contaning other Iterables which is expected to represent a CSV-structured matrix) and a string, and writes the former as the content of a file at the location denoted by the latter (which is assumed to denote a POSIX path). | October 26th, 2024 | October 26th, 2024 |
| 14 | `snippyts.`<br>`__init__.`<br>`from_csv` | Function that can be directed to a local CSV file by its POSIX path and returns the content of that file as a list of lists (or, more geneally, an Iterable contaning other Iterables which is expected to represent a CSV-structured matrix). | October 26th, 2024 | October 26th, 2024 |
| 15 | `snippyts.`<br>`__init__.`<br>`tryline` | Wraps a try-raise block into a single statement. It is intended to flatten try-catch.<br><br>It attempts to call the specified Python-callable object with the provided arguments and keyword arguments.<br><br>If the call is successful, it silently returns the output of the call.<br><br>If it fails, it raises an exception of the type provided as the second argument.| February 28th, 2025 | February 28th, 2025 |
| 16 | `snippyts.`<br>`__init__.`<br>`is_url` | Determines whether a given string is a valid URL.<br><br>It uses urllib.parse.urlparse, a function that splits a URL into six components: scheme, network location, path, parameters, query, and fragment.  | February 28th, 2025 | February 28th, 2025 |
| 17 | `snippyts.`<br>`__init__.`<br>`gtml` | Gets the HTML content of the document at the specified location URL. Named `gtml` as a shorthand for "get HTML". | February 28th, 2025 | February 28th, 2025 |
| 18 | `snippyts.`<br>`preprocessing.`<br>`KBinsEncoder` | Discretizes the data into `n_bins` using scikit-learn's `KBinsDiscretizer` class, and then replaces every input value with the value at the bin-th quantile, ensuring that the output vector<br>- only has `n_bins` unique element but<br>- has the same dimensionality as the original input vector. | February 28th, 2025 | February 28th, 2025 |


# Running tests

### Using `pytest`

Change into the project's home folder (first line below) and run `pytest` (second line). After moving into that directory, the working folder should contain two subfolders, `src` (in turn the parent of subfolder `snippyts`) and `tests`:

```
cd snippyts ;
pytest tests ;
```

### Running the module as a package

```
cd snippyts ;
python -m src.snippyts.__init__ ;
python -m src.snippyts.preprocessing ;
```