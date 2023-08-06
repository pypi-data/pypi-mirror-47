# Ruri
A CRC-32 Cyclic Redundancy Check implementation in Python.
Checks the CRC-32 against a part in the filename.

Previously "Timmy1e/crc32".

## Reqirements
 - Python 3.5+
 - [Progressbar2](https://pypi.python.org/pypi/progressbar2)

## Installation
 1. Pull the project, or download a release python file.
 2. Either copy or link the python file to your `/usr/bin/` or `/usr/local/bin/` directory.
 3. Done.

## Usage
```sh
$ ruri [-h] [-r] [-t THREADS] [-v] [-q] file [file ...]

positional arguments:
  file                  The file(s) you need CRCed

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       work recursively
  -t THREADS, --threads THREADS
                        override the ammount of threads
  -v, --verbose         output level
  -q, --quiet           Do not print progressbars.
  --version             Print the version number, and exit.
```

Basic example:
```sh
$ ruri "myFile[ABCD1234].ext" myFiles*.ext
```

## Licence
GNU General Public License v3.0
