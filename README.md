# snippyts

Miscellaneous utility scripts and Python objects for agile development.


# Table of objects

| No. | Name | Description | Date added | Date reviewed |
| --- | --- | --- | --- | --- |
| 1 | `snippyts.__init__.batched` | Partitions an input collection `iterable` into chunks of size `batch_size`. The number of chunks is unknown at the time of calling is determined by the length of `iterable`. | September 22nd, 2024 | September 22nd, 2024 |
| 2 | `snippyts.__init__.flatten` | Given a collection of lists, concatenates all elements into a single list. More formally, given a collection holding `n` iterables with `m` elements each, this function will return a single list holding all `n * m` elements. | September 22nd, 2024 | September 22nd, 2024 |
| 3 | `create_python_simple_package.sh` | BASH script to initialize a local Python package as a local git repository with a virtual environment, project files, and standard folder structure. It takes user input into account for parameterization from the command line. | September 22nd, 2024 | September 23rd, 2024 |
| 4 | `snippyts.__init__.to_txt` | Function that expects two string parameters as arguments and writes the first string as the content of a file at the location denoted by the second string (which is assumed to denote a POSIX path). | September 23rd, 2024 | September 23rd, 2024 |
| 5 | `snippyts.__init__.from_txt` | Function that can be directed to a local raw text file by its POSIX path and returns the content of that file as a string. | September 23rd, 2024 | September 23rd, 2024 |
| 6 | `snippyts.__init__.to_json` | Function that expects two parameters as arguments, a Python dictionary and a string, and writes the former as the content of a file at the location denoted by the latter (which is assumed to denote a POSIX path). | September 24th, 2024 | September 24th, 2024 |
| 7 | `snippyts.__init__.from_json` | Function that can be directed to a local raw text file by its POSIX path and returns the content of that file as a Python dictionary. | September 24th, 2024 | September 24th, 2024 |