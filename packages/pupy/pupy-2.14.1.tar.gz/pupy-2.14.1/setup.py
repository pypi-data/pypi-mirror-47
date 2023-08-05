# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pupy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pupy',
    'version': '2.14.1',
    'description': 'pretty useful python',
    'long_description': None,
    'author': 'jessekrubin',
    'author_email': 'jessekrubin@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
