# snippyts

Miscellaneous utility scripts and Python objects for agile development.

1. [Table of ojects](#table-of-objects)
2. [Instructions for running tests](#running-tests)


# Table of objects

| No. | Name | Description | Date added | Date reviewed |
| --- | --- | --- | --- | --- |
| 1 | `snippyts.__init__.batched` | Partitions an input collection `iterable` into chunks of size `batch_size`. The number of chunks is unknown at the time of calling is determined by the length of `iterable`. | September 22nd, 2024 | September 22nd, 2024 |
| 2 | `snippyts.__init__.flatten` | Given a collection of lists, concatenates all elements into a single list. More formally, given a collection holding `n` iterables with `m` elements each, this function will return a single list holding all `n * m` elements. | September 22nd, 2024 | September 22nd, 2024 |
| 3 | `create_python_simple_package.sh` | BASH script to initialize a local Python package as a local git repository with a virtual environment, project files, and standard folder structure. It takes user input into account for parameterization from the command line. | September 22nd, 2024 | September 23rd, 2024 |
| 4 | `snippyts.__init__.to_txt` | Function that expects two string parameters as arguments and writes the first string as the content of a file at the location denoted by the second string (which is assumed to denote a POSIX path). | September 23rd, 2024 | September 23rd, 2024 |
| 5 | `snippyts.__init__.from_txt` | Function that can be directed to a local raw text file by its POSIX path and returns the content of that file as a string. | September 23rd, 2024 | September 23rd, 2024 |
| 6 | `snippyts.__init__.to_json` | Function that expects two parameters as arguments, a Python dictionary and a string, and writes the former as the content of a file at the location denoted by the latter (which is assumed to denote a POSIX path). | September 24th, 2024 | September 24th, 2024 |
| 7 | `snippyts.__init__.from_json` | Function that can be directed to a local JSON file by its POSIX path and returns the content of that file as a Python dictionary. | September 24th, 2024 | September 24th, 2024 |
| 8 | `snippyts.__init__.to_pickle` | Function that can be directed to a local raw text file by its POSIX path and returns the content of that file as a Python dictionary. | October 3rd, 2024 | October 3rd, 2024 |
| 9 | `snippyts.__init__.from_pickle` | Function that can be directed to a local Python-pickle file by its POSIX path and returns a copy of the artifact  persisted in that file. | October 3rd, 2024 | October 3rd, 2024 |
| 10 | `snippyts.trie.Trie` | A class implementing a [trie](https://en.wikipedia.org/wiki/Trie) data structure. | October 3rd, 2024 | October 3rd, 2024 |
| 11 | `snippyts.vocabulary_tools.ExactStringMatcher` | A wrapper around `flashtext2` providing a unified application interface shared with `FuzzySet`. | October 12th, 2024 | October 13th, 2024 |
| 12 | `snippyts.vocabulary_tools.FuzzyStringMatcher` | A wrapper around `FuzzySet` providing a unified application interface shared with `flashtext2`. | October 13th, 2024 | October 13th, 2024 |


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
python -m src.snippyts.__init__
```