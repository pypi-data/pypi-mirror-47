# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flake8_nitpick', 'flake8_nitpick.files']

package_data = \
{'': ['*']}

install_requires = \
['attrs',
 'dictdiffer',
 'flake8>=3.0.0',
 'jmespath',
 'python-slugify',
 'pyyaml',
 'requests',
 'toml']

entry_points = \
{'flake8.extension': ['NIP = flake8_nitpick.plugin:NitpickChecker']}

setup_kwargs = {
    'name': 'flake8-nitpick',
    'version': '0.13.0',
    'description': 'Flake8 plugin to enforce the same lint configuration (flake8, isort, mypy, pylint) across multiple Python projects',
    'long_description': '# flake8-nitpick\n\n[![PyPI](https://img.shields.io/pypi/v/flake8-nitpick.svg)](https://pypi.python.org/pypi/flake8-nitpick)\n[![Travis CI](https://travis-ci.com/andreoliwa/flake8-nitpick.svg?branch=master)](https://travis-ci.com/andreoliwa/flake8-nitpick)\n[![Documentation Status](https://readthedocs.org/projects/flake8-nitpick/badge/?version=latest)](https://flake8-nitpick.readthedocs.io/en/latest/?badge=latest)\n[![Coveralls](https://coveralls.io/repos/github/andreoliwa/flake8-nitpick/badge.svg?branch=master)](https://coveralls.io/github/andreoliwa/flake8-nitpick?branch=master)\n[![Maintainability](https://api.codeclimate.com/v1/badges/901b4b62293cf7f2c4bc/maintainability)](https://codeclimate.com/github/andreoliwa/flake8-nitpick/maintainability)\n[![Test Coverage](https://api.codeclimate.com/v1/badges/901b4b62293cf7f2c4bc/test_coverage)](https://codeclimate.com/github/andreoliwa/flake8-nitpick/test_coverage)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/flake8-nitpick.svg)](https://pypi.org/project/flake8-nitpick/)\n[![Project License](https://img.shields.io/pypi/l/flake8-nitpick.svg)](https://pypi.org/project/flake8-nitpick/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=andreoliwa/flake8-nitpick)](https://dependabot.com)\n[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)\n\nFlake8 plugin to enforce the same lint configuration (flake8, isort, mypy, pylint) across multiple Python projects.\n\nA "nitpick code style" is a [TOML](https://github.com/toml-lang/toml) file with settings that should be present in config files from other tools. E.g.:\n\n- `pyproject.toml` and `setup.cfg` (used by [flake8](http://flake8.pycqa.org/), [black](https://black.readthedocs.io/), [isort](https://isort.readthedocs.io/), [mypy](https://mypy.readthedocs.io/));\n- `.pylintrc` (used by [pylint](https://pylint.readthedocs.io/) config);\n- more files to come.\n\n---\n\n- [Installation and usage](#installation-and-usage)\n- [Style file](#style-file)\n- [setup.cfg](#setupcfg)\n\n---\n\n## Installation and usage\n\nSimply install the package (in a virtualenv or globally, wherever) and run `flake8`:\n\n    $ pip install -U flake8-nitpick\n    $ flake8\n\nYou will see warnings if your project configuration is different than [the default style file](https://raw.githubusercontent.com/andreoliwa/flake8-nitpick//0.13.0/nitpick-style.toml/nitpick-style.toml).\n\n## Style file\n\n### Configure your own style file\n\nChange your project config on `pyproject.toml`, and configure your own style like this:\n\n    [tool.nitpick]\n    style = "https://raw.githubusercontent.com/andreoliwa/flake8-nitpick//0.13.0/nitpick-style.toml/nitpick-style.toml"\n\nYou can set `style` with any local file or URL. E.g.: you can use the raw URL of a [GitHub Gist](https://gist.github.com).\n\nYou can also use multiple styles and mix local files and URLs:\n\n    [tool.nitpick]\n    style = ["/path/to/first.toml", "/another/path/to/second.toml", "https://example.com/on/the/web/third.toml"]\n\nThe order is important: each style will override any keys that might be set by the previous .toml file.\nIf a key is defined in more than one file, the value from the last file will prevail.\n\n### Default search order for a style file\n\n1. A file or URL configured in the `pyproject.toml` file, `[tool.nitpick]` section, `style` key, as [described above](#configure-your-own-style-file).\n\n2. Any `nitpick-style.toml` file found in the current directory (the one in which `flake8` runs from) or above.\n\n3. If no style is found, then [the default style file from GitHub](https://raw.githubusercontent.com/andreoliwa/flake8-nitpick//0.13.0/nitpick-style.toml/nitpick-style.toml) is used.\n\n### Style file syntax\n\nA style file contains basically the configuration options you want to enforce in all your projects.\n\nThey are just the config to the tool, prefixed with the name of the config file.\n\nE.g.: To [configure the black formatter](https://github.com/ambv/black#configuration-format) with a line length of 120, you use this in your `pyproject.toml`:\n\n    [tool.black]\n    line-length = 120\n\nTo enforce that all your projects use this same line length, add this to your `nitpick-style.toml` file:\n\n    ["pyproject.toml".tool.black]\n    line-length = 120\n\nIt\'s the same exact section/key, just prefixed with the config file name (`"pyproject.toml".`)\n\nThe same works for `setup.cfg`.\nTo [configure mypy](https://mypy.readthedocs.io/en/latest/config_file.html#config-file-format) to ignore missing imports in your project:\n\n    [mypy]\n    ignore_missing_imports = true\n\nTo enforce all your projects to ignore missing imports, add this to your `nitpick-style.toml` file:\n\n    ["setup.cfg".mypy]\n    ignore_missing_imports = true\n\n### Absent files\n\nTo enforce that certain files should not exist in the project, you can add them to the style file.\n\n    [[files.absent]]\n    file = "myfile1.txt"\n\n    [[files.absent]]\n    file = "another_file.env"\n    message = "This is an optional extra string to display after the warning"\n\nMultiple files can be configured as above.\nThe `message` is optional.\n\n## setup.cfg\n\n### Comma separated values\n\nOn `setup.cfg`, some keys are lists of multiple values separated by commas, like `flake8.ignore`.\n\nOn the style file, it\'s possible to indicate which key/value pairs should be treated as multiple values instead of an exact string.\nMultiple keys can be added.\n\n    ["setup.cfg".nitpick]\n    comma_separated_values = ["flake8.ignore", "isort.some_key", "another_section.another_key"]\n',
    'author': 'W. Augusto Andreoli',
    'author_email': 'andreoliwa@gmail.com',
    'url': 'https://github.com/andreoliwa/flake8-nitpick',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
