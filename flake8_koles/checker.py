"""Koles checker module."""
import ast
import optparse
import os
import re
from typing import Generator, List, Set, Tuple

import pkg_resources
from flake8.options.manager import OptionManager
from flake8.utils import stdin_get_value
from pycodestyle import readlines

from flake8_koles import __version__


class KolesChecker:
    """Bad language checker class."""

    name = 'flake8-koles'
    options = None
    swear_list_dir = '/data/swear_list'
    version = __version__

    def __init__(self, tree: ast.Module, filename: str) -> None:
        """Initialize class values. Parameter `tree` is required by flake8."""
        self.filename = filename
        self._pattern = '|'.join(self._get_bad_words())

    def run(self) -> Generator[Tuple[int, int, str, type], None, None]:
        """Run the linter and return a generator of errors."""
        content = self._get_file_content()
        yield from self._get_filename_errors()
        yield from self._get_content_errors(content)

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        """Add koles linter options to the flake8 parser."""
        parser.add_option(
            '--ignore-shorties',
            default=0,
            type='int',
            parse_from_config=True
        )
        parser.add_option(
            '--censor-msg',
            default=0,
            parse_from_config=True,
            action='store_true'
        )
        parser.add_option(
            '--lang',
            default='english',
            parse_from_config=True,
            comma_separated_list=True
        )

    @classmethod
    def parse_options(cls, options: optparse.Values) -> None:
        """Get parser options from flake8."""
        cls.options = options

    def _check_row(self, string: str) -> List[Tuple[int, str]]:
        """Return a list containing bad words and their positions."""
        if self._pattern == '':
            return []

        regex = re.compile(f'(?=({self._pattern}))', flags=re.IGNORECASE)

        return [
            (match.start(), match.group(1))
            for match in regex.finditer(string)
        ]

    def _get_bad_words(self) -> Set[str]:
        """Get a set of bad words."""
        data = self._get_swears_data()

        return {
            word
            for word in data.decode().strip().split('\n')
            if len(word) > self.options.ignore_shorties  # type: ignore
        }

    def _get_swears_data(self) -> bytes:
        """Get swears data from languages present in the options."""
        data = b''
        for lang in self.options.lang:  # type: ignore
            file_path = f'{self.swear_list_dir}/{lang}.dat'
            data += pkg_resources.resource_string(
                __name__, file_path
            )

        return data

    def _get_file_content(self) -> List[str]:
        """Return file content as a list of lines."""
        if self.filename in ('stdin', '-', None):
            return stdin_get_value().splitlines(True)
        else:
            return readlines(self.filename)

    def _censor_word(self, word: str) -> str:
        """Replace all letters but first with `*` if censor_msg option is True."""
        if self.options.censor_msg:  # type: ignore
            return word[0] + '*' * (len(word) - 1)
        return word

    def _get_filename_errors(self) -> Generator[Tuple[int, int, str, type], None, None]:
        """Get filename errors if exist."""
        filename_errors = self._check_row(os.path.basename(self.filename))

        return (
            (
                0,
                column,
                f'KOL002 Filename contains bad language: {self._censor_word(word)}',
                KolesChecker,
            )
            for column, word in filename_errors
        )

    def _get_content_errors(
            self, content
    ) -> Generator[Tuple[int, int, str, type], None, None]:
        """Get file content errors if any exist."""
        for row_number, row in enumerate(content, 1):
            errors = self._check_row(row)
            yield from (
                (
                    row_number,
                    column,
                    f'KOL001 Bad language found: {self._censor_word(word)}',
                    KolesChecker,
                )
                for column, word in errors
            )
