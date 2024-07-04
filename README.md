# fastlid
<!--- repo_name  pack_name  mod_name func_name --->
[![tests](https://github.com/ffreemt/fast-langid/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/fastlid.svg)](https://badge.fury.io/py/fastlid)

Language identification based on fasttext (lid.176.ftz https://fasttext.cc/docs/en/language-identification.html).

The `lid.176.ftz` file is licensed under  Creative Commons Attribution-Share-Alike License 3.0 and is not part of this module. It is automatically downloaded from its external origin on the first run of this module.

This module attempts to immitate the follow two features of `langid`
*   langid.classify: fastlid
*   langid.set_languages(langs=[...]): fastlid.set_languages = [...]
    *   import fastlid
    *   fastlid.set_languages = ['nl','fr'])
*   TODO: Commandline interface

## Preinstall fasttext

For Linux and friends (Mac for exmaple)
```
pip install fasttext
```

For Windows:

```bash
pip install fasttext-wheel
```
or (for python 3.8)
```
pip install https://github.com/ffreemt/ezbee/raw/main/data/artifects/fasttext-0.9.2-cp38-cp38-win_amd64.whl
```

## Install it

```bash
pip install fastlid
```
or install from `git`
```bash
pip install git+https://github.com/ffreemt/fast-langid.git

# also works pip install git+https://github.com/ffreemt/fast-langid
```
or clone the git repo and install from source.

## Use it
```python
from fastlid import fastlid, supported_langs

# support 176 languages
print(supported_langs, len(supported_langs))
# ['af', 'als', 'am', 'an', 'ar', 'arz', 'as', 'ast', 'av', 'az'] 176

fastlid("test this")
# ('en', 0.765)

fastlid("test this 测试一下", k=2)
# (['zh', 'en'], [0.663, 0.124])

fastlid.set_languages = ['fr', 'zh']
fastlid("test this 测试吧")
# ('zh', 0.01)

fastlid.set_languages = None
fastlid("test this 测试吧")
('en', 0.686)

fastlid.set_languages = ['fr', 'zh', 'en']
fastlid("test this 测试吧", k=3)
(['en', 'zh', 'fr'], [0.686, 0.01, 0.006])
```

N.B. `hanzidentifier` can be used to identify simplified Chinese or/and traditional Chinese should you need to do so.

## For Developers
Install `poetry` and `yarn` the way you like it.
```bash
poetry install  # install python packages
yarn install --dev  # install necesary node packages

# ...code...
yarn test
yarn final

# ...optionally submit pr...
```