# flake8-koles

[![Build Status](https://travis-ci.org/myslak71/flake8-koles.svg?branch=master)](https://travis-ci.org/myslak71/flake8-koles)
[![Coverage Status](https://coveralls.io/repos/github/myslak71/flake8-koles/badge.svg?branch=master)](https://coveralls.io/github/myslak71/flake8-koles?branch=master)
![image](https://img.shields.io/badge/python-3.7-blue.svg)
![image](https://img.shields.io/badge/version-0.1.0-yellow)

Watch your language young pal!

Flake8 extension for checking bad language occurrences. Lists all swears found in the code and their location.
For now only english language is supported.

## Installation
flake8 is required for the installation.
```
pip install flake8-koles
```

## Usage
```
flake8 --ignore-shorties 4 --censor-msg
```
`--ignore-shorties <number>` - ignores bad words shorter or equal to `<number>`

`--censor-msg` - replaces bad words not leading letters with `*` in error messages

## Development notes
`make lint` - runs all linters

`make flake8` - runs flake8

`make unittests` - runs unittests with coverage report and -s flag

`make mypy` - runs mypy

`make yamllint` - runs yamllint
