# flake8-koles

[![Build Status](https://travis-ci.org/myslak71/flake8-koles.svg?branch=master)](https://travis-ci.org/myslak71/flake8-koles)
[![Coverage Status](https://coveralls.io/repos/github/myslak71/flake8-koles/badge.svg?branch=master)](https://coveralls.io/github/myslak71/flake8-koles?branch=master)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/flake8-koles)
![image](https://img.shields.io/badge/version-0.2.1-yellow)
![Requires.io](https://img.shields.io/requires/github/myslak71/flake8-koles)
![GitHub](https://img.shields.io/github/license/myslak71/flake8-koles?color=46c28e)

Watch your language young pal!

Flake8 extension for checking bad language occurrences. Lists all swears found in the code and their location.
For now only english and polish languages are supported.

## Installation
flake8>=3.3.0 is required for the installation.
```
pip install flake8-koles
```

## Usage
```
flake8 --ignore-shorties 4 --censor-msg --lang=english,polish --ignore-swears=very,bad,words
```
##### Options
|OPTION    | DEFAULT|DESCRIPTION |
| --------  |---|-------------|
|`--censor-msg`|False |replace swears not leading letters with `*` in error messages|
|`--ignore-shorties`|0 |ignore swears shorter or equal to the argument|
|`--ignore-swears`| |explicitly pass swears to ignore|
|`--lang`|english |use swears from the selected languages|

Above options may be specified in `setup.cfg` file as well.

## Development notes

##### Makefile commands

|COMMAND |DESCRIPTION|
|--------|-----------|
|`make coverage_html`|generate and open html coverage report in the default browser|
|`make flake8`|run flake8|
|`make mypy`|run mypy|
|`make lint`|run all linters|
|`make safety`|run safety check|
|`make unittests`|run unittests with coverage report
|`make yamllint`|run yamllint|
