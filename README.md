# flake8-koles

[![Build Status](https://travis-ci.org/myslak71/flake8-koles.svg?branch=master)](https://travis-ci.org/myslak71/flake8-koles)
[![Coverage Status](https://coveralls.io/repos/github/myslak71/flake8-koles/badge.svg?branch=master)](https://coveralls.io/github/myslak71/flake8-koles?branch=master)
![image](https://img.shields.io/badge/python-3.7-blue.svg)
![image](https://img.shields.io/badge/version-0.1.2-yellow)

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
flake8 --ignore-shorties 4 --censor-msg --lang=english,polish
```
##### Options
|OPTION    | DEFAULT|DESCRIPTION |
| --------  |---|-------------|
|`--ignore-shorties`|0 |ignore bad words shorter or equal to the argument|
|`--censor-msg`|False |replace bad words not leading letters with `*` in error messages|
|`--lang`|english |use bad words from the selected languages|

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
