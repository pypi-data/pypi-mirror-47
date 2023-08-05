# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['status_map']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'status-map',
    'version': '0.1.0',
    'description': 'Status map (and its transitions) data structure',
    'long_description': None,
    'author': 'Luiz Menezes',
    'author_email': 'luiz.menezesf@gmail.com',
    'url': 'https://github.com/lamenezes/django-choices-enum',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
