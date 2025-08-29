# snippyts

Miscellaneous utility scripts and Python objects for agile development.

1. [Table of objects](#table-of-objects)
2. [Change log](#change-log)
3. [Instructions for running tests](#Running-tests)


# Table of objects

| No. | Name | Description | Date added | Date reviewed |
| --- | --- | --- | --- | --- |
| 1 | `snippyts.`<br>`__init__.`<br>`batched` | Partitions an input collection `iterable` into chunks of size `batch_size`. The number of chunks is unknown at the time of calling is determined by the length of `iterable`. | 2024 Sep 22 | 2024 Sep 22 |
| 2 | `snippyts.`<br>`__init__.`<br>`flatten` | Given a collection of lists, concatenates all elements into a single list. More formally, given a collection holding `n` iterables with `m` elements each, this function will return a single list holding all `n * m` elements. | 2024 Sep 22 | 2024 Sep 22 |
| 3 | `create_python_`<br>`simple_package.sh` | BASH script to initialize a local Python package as a local git repository with a virtual environment, project files, and standard folder structure. It takes user input into account for parameterization from the command line. | 2024 Sep 22 | 2024 Sep 23 |
| 4 | `snippyts.`<br>`__init__.`<br>`to_txt` | Function that expects two string parameters as arguments and writes the first string as the content of a file at the location denoted by the second string (which is assumed to denote a POSIX path). | 2024 Sep 23 | 2024 Sep 23 |
| 5 | `snippyts.`<br>`__init__.`<br>`from_txt` | Function that can be directed to a local raw text file by its POSIX path and returns the content of that file as a string. | 2024 Sep 23 | 2024 Sep 23 |
| 6 | `snippyts.`<br>`__init__.`<br>`to_json` | Function that expects two parameters as arguments, a Python dictionary and a string, and writes the former as the content of a file at the location denoted by the latter (which is assumed to denote a POSIX path). | 2024 Sep 24 | 2024 Sep 24 |
| 7 | `snippyts.`<br>`__init__.`<br>`from_json` | Function that can be directed to a local JSON file by its POSIX path and returns the content of that file as a Python dictionary. | 2024 Sep 24 | 2024 Sep 24 |
| 8 | `snippyts.`<br>`__init__.`<br>`to_pickle` | Function that can be directed to a local raw text file by its POSIX path and returns the content of that file as a Python dictionary. | 2024 Oct 03 | 2024 Oct 03 |
| 9 | `snippyts.`<br>`__init__.`<br>`from_pickle` | Function that can be directed to a local Python-pickle file by its POSIX path and returns a copy of the artifact  persisted in that file. | 2024 Oct 03 | 2024 Oct 03 |
| 10 | `snippyts.trie.Trie` | A class implementing a [trie](https://en.wikipedia.org/wiki/Trie) data structure. | 2024 Oct 03 | **2025 Aug 27** |
| 11 | `snippyts.`<br>`vocabulary_tools.`<br>`ExactStringMatcher` | A wrapper around `flashtext2` providing a unified application interface shared with `FuzzySet`. | 2024 Oct 12 | 2024 Oct 26 |
| 12 | `snippyts.`<br>`vocabulary_tools.`<br>`FuzzyStringMatcher` | A wrapper around `FuzzySet` providing a unified application interface shared with `flashtext2`. | 2024 Oct 13 | 2024 Oct 26 |
| 13 | `snippyts.`<br>`__init__.`<br>`to_csv` | Function that expects two parameters as arguments, a list of lists (or, more geneally, an Iterable contaning other Iterables which is expected to represent a CSV-structured matrix) and a string, and writes the former as the content of a file at the location denoted by the latter (which is assumed to denote a POSIX path). | 2024 Oct 26 | 2024 Oct 26 |
| 14 | `snippyts.`<br>`__init__.`<br>`from_csv` | Function that can be directed to a local CSV file by its POSIX path and returns the content of that file as a list of lists (or, more geneally, an Iterable contaning other Iterables which is expected to represent a CSV-structured matrix). | 2024 Oct 26 | 2024 Oct 26 |
| 15 | `snippyts.`<br>`__init__.`<br>`tryline` | Wraps a try-raise block into a single statement. It is intended to flatten try-catch.<br><br>It attempts to call the specified Python-callable object with the provided arguments and keyword arguments.<br><br>If the call is successful, it silently returns the output of the call.<br><br>If it fails, it raises an exception of the type provided as the second argument.| 2025 Feb 28 | 2025 Feb 28 |
| 16 | `snippyts.`<br>`__init__.`<br>`is_url` | Determines whether a given string is a valid URL.<br><br>It uses urllib.parse.urlparse, a function that splits a URL into six components: scheme, network location, path, parameters, query, and fragment.  | 2025 Feb 28 | 2025 Feb 28 |
| 17 | `snippyts.`<br>`__init__.`<br>`gtml` | Gets the HTML content of the document at the specified location URL. Named `gtml` as a shorthand for "get HTML". | 2025 Feb 28 | 2025 Feb 28 |
| 18 | `snippyts.`<br>`preprocessing.`<br>`KBinsEncoder` | Discretizes the data into `n_bins` using scikit-learn's `KBinsDiscretizer` class, and then replaces every input value with the value at the bin-th quantile, ensuring that the output vector<br>- only has `n_bins` unique element but<br>- has the same dimensionality as the original input vector. | 2025 Feb 28 | **2025 Aug 23** |
| 19 | `snippyts.`<br>`__init__.`<br>`to_yaml` | Works like `to_txt` but writes out YAML-formatted data. | **2025 Jul 27** | **2025 Jul 27** |
| 20 | `snippyts.`<br>`__init__.`<br>`cp` | Shorthand for `copy.deepcopy`. | **2025 Jul 27** | **2025 Jul 27** |
| 21 | `snippyts.`<br>`__init__.`<br>`from_yaml` | Works like `from_yaml` but reads in YAML-formatted data into a Python dictionary object. | **2025 Jul 27** | **2025 Jul 27** |
| 22 | `snippyts.`<br>`__init__.`<br>`defolder` | Function that takes a path string as an argument. If a folder at that path does not exist yet, it gets created. It then returns the real path of the folder, resolving any symbolic links in the path if they exist. File names are implicitly parsed for their containing folder names; the folder name is handled as per the specifications but the final path returned by the function will include again the file name. | **2025 Jul 27** | **2025 Jul 27** |
| 23 | `snippyts.`<br>`metrics.`<br>`average_token_similarity` | Given two strings, it greedily and fuzzily aligns their tokens by similarity and returns the similarity ratio for the full sequence averaged over all tokens. | **2025 Jul 28** | **2025 Jul 28** |
| 24 | `snippyts.`<br>`__init__.`<br>`UnsupportedInputShapeError` | Self-explanatory exception. | **2025 AUG 1** | **2025 AUG 1** |
| 25 | `snippyts.`<br>`__init__.`<br>`smart_cast_number` | Cast a numeric value to an integer if it is numerically whole; otherwise, return as float. | **2025 AUG 1** | **2025 AUG 1** |
| 26 | `snippyts.`<br>`__init__.`<br>`is_number` | Function that checks whether a string can be interpreted as a integer or a float. | **2025 AUG 1** | **2025 AUG 1** |
| 27 | `snippyts.`<br>`__init__.`<br>`read_arg` | Function that reads command line arguments passed to a python script, then returns the corresponding value of the specified argument's name. | **2025 JUL 27** | **2025 JUL 27** |
| 28 | `snippyts.`<br>`__init__.`<br>`read_args` | Function that reads all named command line arguments passed to a Python script (names are those starting with `-` or `--`), then saves their corresponding values into a namedtuple. <br><br>The argument names are converted into valid attribute names by stripping leading hyphens and replacing non-alpha-numeric characters with underscores. | **2025 JUL 27** | **2025 JUL 27** |

## Change log

### 2025 AUG

**NLP & ML**

1. Fixes `snippyts.trie.Trie`.2. Fixes `snippyts.preprocessing.KBinsEncoder`.3. Adds `snippyts.metrics.average_token_similarity`, a function for calculating the average token similarity between two strings.
**I/O Functions**
3. Adds `snippyts.__init__.to_yaml`, a function for writing out YAML-formatted data.
5. Adds `snippyts.__init__.from_yaml`, a function that reads in YAML-formatted data into a Python dictionary.
5. Adds `snippyts.__init__.read_arg`, a function that returns the value of a specified command-line parameter name (names are those starting with `-` or `--`).
6. Adds `snippyts.__init__.read_args`, like `read_arg` but for applies implicitly to all parameters and returns their arguments as values in a `namedtuple`, with the parameter name as the attributes.

**System & Language**
2. Adds `snippyts.__init__.cp`, a shorthand for `copy.deepcopy`.
1. Adds `snippyts.__init__.smart_cast_number`, a function for casting a numeric value to an integer if it is numerically whole; otherwise, return as float.
1. Adds `snippyts.__init__.is_number`, a function that checks whether a string can be interpreted as a integer or a float.3. Adds `snippyts.__init__.defolder`, a function that handles path strings and creates folders if they do not exist yet.4. Adds `snippyts.__init__.UnsupportedInputShapeError`, an exception for handling unsupported input shapes.


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