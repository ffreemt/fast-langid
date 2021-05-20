# fastlid
<!--- repo_name  pack_name  mod_name func_name --->
[![tests](https://github.com/ffreemt/fast-langid/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/fastlid.svg)](https://badge.fury.io/py/fastlid)

Language identification based on fasttext (lid.176.ftz https://fasttext.cc/docs/en/language-identification.html).

The lid.176.ftz is licensed under CC-BY-SA and is not part of this module. It is automatically downloaded from its external origin on the first run of this module.

This module attempts to immitate the follow two features of `langid`
*   fastlid.classify
*   fastlid.set_languages
    *   import fastlid
    *   fastlid.set_languages(langs=['nl','fr'])
*   TODO: Commandline interface

## Install it
```bash
pip install fastlid
```
or install from `git`
```bash
pip install git+https://github.com/ffreemt/fast-langid.git
```
or clone the git repo and install from source.

## Use it
```python
from fastlid import fastlid
```

## For Developers
Install `poetry` and `yarn` the way you like it.
```bash
poetry install --dev
yarn install --dev

yarn test
yarn final
```