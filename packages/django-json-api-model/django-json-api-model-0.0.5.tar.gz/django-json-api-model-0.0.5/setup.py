import os
import re

from setuptools import find_packages, setup

with open('./jam/__init__.py') as f:
    exec(re.search(r'VERSION = .*', f.read(), re.DOTALL).group())

setup(
    name='django-json-api-model',
    version=__version__,
    author='Luke Hodkinson',
    author_email='luke.hodkinson@uptickhq.com',
    maintainer='Uptick',
    maintainer_email='dev@uptickhq.com',
    url='https://github.com/uptick/django-jam',
    description='',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.js', '*.html', '*.*']},
    install_requires=[
        'setuptools',
        'inflection'
    ],
)
