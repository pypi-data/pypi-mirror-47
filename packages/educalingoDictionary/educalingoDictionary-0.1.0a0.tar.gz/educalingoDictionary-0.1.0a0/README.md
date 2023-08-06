# Educalingo Dictionary — Package

[![Build Status](https://travis-ci.org/JessicaSousa/EducalingoDictionary.svg?branch=master)](https://travis-ci.org/JessicaSousa/EducalingoDictionary)
[![codecov]( https://codecov.io/gh/JessicaSousa/EducalingoDictionary/branch/master/graph/badge.svg)](https://codecov.io/gh/JessicaSousa/EducalingoDictionary)
[![GitHub license](https://img.shields.io/github/license/JessicaSousa/EducalingoDictionary.svg)](https://github.com/JessicaSousa/EducalingoDictionary/blob/master/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/educalingoDictionary.svg)](https://pypi.org/project/educalingoDictionary/)

The ``educalingoDictionary`` Package is a basic package written in Python can download the info from the [Educalingo Dictionary](http://educalingo.com/).

## Installation

You can install, upgrade, and uninstall  the ``educalingoDictionary`` with these commands:
```console
$ pip install educalingoDictionary
$ pip install --upgrade educalingoDictionary
$ pip uninstall educalingoDictionary
```
## Usage
```python
from educalingoDictionary import EducalingoDictionary
my_dictionary = EducalingoDictionary()
my_dictionary.set_language("pt")
```
Performing a dictionary search for the _legal_ (nice) word.
```python
from educalingoDictionary import EducalingoDictionary
my_dictionary = EducalingoDictionary()
# setting language to Portuguese
my_dictionary.set_language("pt")
my_dictionary.search_word(word="legal")
```

Get the list of synonyms through the ``get_synonyms`` method.

```python
from educalingoDictionary import EducalingoDictionary
my_dictionary = EducalingoDictionary()
# setting language to Portuguese
my_dictionary.set_language("pt")
my_dictionary.search_word(word="legal")
# get list of synonyms of "legal"
synonyms = my_dictionary.get_synonyms()
```

## Available dictionaries
 * **bn**: 'Bengali dictionary',
 * **de**: 'German dictionary',
 * **en**: 'English dictionary',
 * **es**: 'Spanish dictionary',
 * **fr**: 'French dictionary',
 * **hi**: 'Hindi dictionary',
 * **it**: 'Italian dictionary',
 * **ja**: 'Japanese dictionary',
 * **jv**: 'Javanese dictionary',
 * **ko**: 'Korean dictionary',
 * **mr**: 'Marathi dictionary',
 * **ms**: 'Malay dictionary',
 * **pl**: 'Polish dictionary',
 * **pt**: 'Portuguese dictionary',
 * **ro**: 'Romanian dictionary',
 * **ru**: 'Russian dictionary',
 * **ta**: 'Tamil dictionary',
 * **tr**: 'Turkish dictionary',
 * **uk**: 'Ukrainian dictionary',
 * **zh**: 'Chinese dictionary'