"""Koles package installation setup."""
import os

from setuptools import setup

DIR_PATH = os.path.abspath(os.path.dirname(__file__))

install_requires = ['flake8>=1.5', 'six', 'pycodestyle']

with open(os.path.join(DIR_PATH, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()

about = {}

with open(os.path.join(DIR_PATH, 'flake8_koles', '__about__.py'), 'r', encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name=about['__title__'],
    description=about['__description__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=about['__version__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    license=about['__license__'],
    keywords=about['__keywords__'],
    download_url=about['__download_url__'],
    packages=['flake8_koles'],
    package_data={'flake8_koles': ['data/swear_list/*.dat']},
    py_modules=['flake8_koles'],
    python_requires=">=3.7",
    install_requires=install_requires,
    entry_points={
        'flake8.extension': [
            'KOL = flake8_koles.checker:KolesChecker',
        ]
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
    ],
)
