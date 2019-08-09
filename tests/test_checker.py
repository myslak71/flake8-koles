"""KolesChecker test module."""
from unittest import mock
from unittest.mock import Mock

import pytest
from flake8.options.manager import Option, OptionManager

from flake8_koles.checker import KolesChecker


@mock.patch('flake8_koles.checker.readlines')
@mock.patch('flake8_koles.checker.KolesChecker._get_pattern')
def test_run(mock_get_pattern, mock_readlines):
    """Test that flake interface returns appropriate error messages."""
    mock_get_pattern.return_value = 'very|bad|words'
    mock_readlines.return_value = ['Test very', 'nice', 'and bad words']
    koles_checker = KolesChecker(tree='test_tree', filename='test_filename')
    koles_checker.options = Mock(censor_msg=True)
    result = [*koles_checker.run()]

    assert result == [
        (1, 5, 'KOL001 Bad language found: v***', KolesChecker),
        (3, 4, 'KOL001 Bad language found: b**', KolesChecker),
        (3, 8, 'KOL001 Bad language found: w****', KolesChecker),
    ]


def test_add_options(koles_checker):
    """Test that all options are added to the parser."""
    option_manager = OptionManager()
    koles_checker.add_options(option_manager)
    assert repr(option_manager.options) == repr(
        [
            Option(
                long_option_name='--censor-msg',
                default=0,
                parse_from_config=True,
                action='store_true',
            ),
            Option(
                long_option_name='--ignore-shorties',
                default=0,
                type='int',
                parse_from_config=True,
            ),
            Option(
                long_option_name='--ignore-swears',
                default='',
                parse_from_config=True,
                comma_separated_list=True,
            ),
            Option(
                long_option_name='--lang',
                default='english',
                parse_from_config=True,
                comma_separated_list=True,
            ),
        ]
    )


def test_parse_options(koles_checker):
    """Test that options are correctly assigned to the class."""
    test_options = {'kick_it': True}
    koles_checker.parse_options(test_options)

    assert koles_checker.options == test_options


@pytest.mark.parametrize(
    "ignore_shorties, ignore_swears, expected_result, get_swears_data_value",
    (
        (0, [], ['Mike D', 'MCA', 'Ad-Rock'], b'Mike D\nMCA\nAd-Rock\n'),
        (1, [], ['Mike D', 'MCA', 'Ad-Rock'], b'Mike D\nMCA\nAd-Rock\n'),
        (3, [], ['Mike D', 'Ad-Rock'], b'Mike D\nMCA\nAd-Rock\n'),
        (6, [], ['Ad-Rock'], b'Mike D\nMCA\nAd-Rock\n'),
        (69, [], [], b'Mike D\nMCA\nAd-Rock\n'),
        # Case: repeated swears, distinct ones returned
        (0, [], ['Mike D', 'MCA', 'Ad-Rock'], b'Mike D\nMCA\nAd-Rock\nMike D\nMCA\n'),
        # Case: ignore word is present
        (0, ['MCA'], ['Mike D', 'Ad-Rock'], b'Mike D\nMCA\nAd-Rock\n'),
        # Case: all swears are ignored
        (0, ['Ad-Rock', 'MCA', 'Mike D'], [], b'Mike D\nMCA\nAd-Rock\n'),
    ),
)
@mock.patch('flake8_koles.checker.KolesChecker._get_swears_data')
def test_get_pattern(
    mock_get_swears_data,
    ignore_shorties,
    ignore_swears,
    expected_result,
    get_swears_data_value,
    koles_checker,
):
    """
    Test _get_bad_words.

    Test that the function returns proper set of bad words
    depending on the ignore-shorties option.
    """
    mock_get_swears_data.return_value = get_swears_data_value
    koles_checker.options = Mock(
        ignore_shorties=ignore_shorties, ignore_swears=ignore_swears
    )
    result = koles_checker._get_pattern()

    assert result.count('|') == max(len(expected_result) - 1, 0)
    assert all((word in result for word in expected_result))


@pytest.mark.parametrize(
    "lang, resource_string_value, expected_result",
    (
        # Case 1: One language
        (['beastie_boys_lang'], [b'Mike D\nMCA\nAd-Rock\n'], b'Mike D\nMCA\nAd-Rock\n'),
        # Case 2: Two languages
        (
            ['beastie_boys_lang', 'snoop_dogg_lang'],
            [b'Mike D\nMCA\nAd-Rock\n', b'Snoop Dogg\nDr. Dre\n'],
            b'Mike D\nMCA\nAd-Rock\nSnoop Dogg\nDr. Dre\n',
        ),
    ),
)
@mock.patch('flake8_koles.checker.pkg_resources.resource_string')
def test_get_swears_data(
    mock_resource_string, lang, resource_string_value, expected_result, koles_checker
):
    """
    Test that _get_swear_data merges swears from languages given in the options.
    """
    mock_resource_string.side_effect = resource_string_value
    koles_checker.options = Mock(lang=lang)
    result = koles_checker._get_swears_data()

    assert result == expected_result


@pytest.mark.parametrize('filename,', ('stdin', '-', None))
@mock.patch('flake8_koles.checker.stdin_get_value')
def test_get_file_content_stdin(mock_stdin_get_value, filename, koles_checker):
    """Test that flake8 stdin_get_value is called for appropriate filename."""
    koles_checker.filename = filename
    koles_checker._get_file_content()

    mock_stdin_get_value.assert_called_once()


@mock.patch('flake8_koles.checker.readlines')
def test_get_file_content_regular_filename(mock_readlines, koles_checker):
    """Test that flake8 pycodestyle readlines is called for appropriate filename."""
    koles_checker.filename = 'test_filename'
    koles_checker._get_file_content()

    mock_readlines.assert_called_once()


@pytest.mark.parametrize(
    'filename, check_row_value, censor_word_value, expected_result',
    (
        ('test_filename', [], [], []),
        (
            'ugly_name',
            [(0, 'ugly')],
            ['ugly'],
            [(0, 0, 'KOL002 Filename contains bad language: ugly', KolesChecker)],
        ),
        (
            'bad_ugly_name',
            [(0, 'bad'), (4, 'ugly')],
            ['bad', 'ugly'],
            [
                (0, 0, 'KOL002 Filename contains bad language: bad', KolesChecker),
                (0, 4, 'KOL002 Filename contains bad language: ugly', KolesChecker),
            ],
        ),
    ),
)
@mock.patch('flake8_koles.checker.KolesChecker._check_row')
@mock.patch('flake8_koles.checker.KolesChecker._censor_word')
def test_get_filename_errors(
    mock_censor_word,
    mock_check_row,
    filename,
    check_row_value,
    censor_word_value,
    expected_result,
    koles_checker,
):
    """Test that appropriate error messages are returned."""
    mock_check_row.return_value = check_row_value
    mock_censor_word.side_effect = censor_word_value
    koles_checker.filename = filename
    result = [*koles_checker._get_filename_errors()]

    assert result == expected_result


@pytest.mark.parametrize(
    'content, check_row_value, censor_word_value, expected_result',
    (
        (['nice_content'], [[]], [], []),
        (
            ['ugly_content'],
            [[(0, 'ugly')]],
            ['ugly'],
            [(1, 0, 'KOL001 Bad language found: ugly', KolesChecker)],
        ),
        (
            ['ugly_content', 'very_bad_content'],
            [[(0, 'ugly')], [(5, 'bad')]],
            ['ugly', 'bad'],
            [
                (1, 0, 'KOL001 Bad language found: ugly', KolesChecker),
                (2, 5, 'KOL001 Bad language found: bad', KolesChecker),
            ],
        ),
    ),
)
@mock.patch('flake8_koles.checker.KolesChecker._check_row')
@mock.patch('flake8_koles.checker.KolesChecker._censor_word')
def test_get_content_errors(
    mock_censor_word,
    mock_check_row,
    content,
    check_row_value,
    censor_word_value,
    expected_result,
    koles_checker,
):
    """Test that appropriate error messages are returned."""
    mock_check_row.side_effect = check_row_value
    mock_censor_word.side_effect = censor_word_value
    result = [*koles_checker._get_content_errors(content)]

    assert result == expected_result


@pytest.mark.parametrize(
    'pattern, string, expected_result',
    (
        # Case 1: Multiple overlapping patterns
        ('abcd|ab|abc|cd', 'abcdab', [(0, 'abcd'), (2, 'cd'), (4, 'ab')]),
        # Case 2: Single non-overlapping pattern
        ('ab', 'abcdab', [(0, 'ab'), (4, 'ab')]),
        # Case 3: Empty string
        ('(?=(ab))', '', []),
        # Case 4: Empty pattern
        ('', 'abcdab', []),
        # Case 6: Empty string and pattern
        ('', '', []),
        # Case 7: Uppercase string
        ('abcd|ab|abc|cd', 'ABCDAB', [(0, 'ABCD'), (2, 'CD'), (4, 'AB')]),
    ),
)
def test_check_row(pattern, string, expected_result, koles_checker):
    """Test that check_string returns appropriate value for given pattern and string."""
    koles_checker._pattern = pattern
    result = koles_checker._check_row(string)

    assert [*result] == expected_result


@pytest.mark.parametrize(
    'word, censor_msg, expected_result',
    (
        ('Mike D', True, 'M*****'),
        ('Mike D', False, 'Mike D'),
        ('MCA', True, 'M**'),
        ('MCA', False, 'MCA'),
        ('Ad-Rock', True, 'A******'),
        ('Ad-Rock', False, 'Ad-Rock'),
    ),
)
def test_censor_word(word, censor_msg, expected_result, koles_checker):
    """Test censor_word.

    Test that the function returns proper set of bad words
    depending on ignore-shorties option.
    """
    koles_checker.options = Mock(censor_msg=censor_msg)
    result = koles_checker._censor_word(word)

    assert result == expected_result


@pytest.mark.parametrize(
    'listdir_value, expected_result',
    (
        # Case: empty language dir
        ([], []),
        (['english.dat'], ['english']),
        (
            ['english.dat', 'polish.dat'],
            ['english', 'polish', 'english,polish', 'polish,english'],
        ),
    ),
)
@mock.patch('flake8_koles.checker.pkg_resources.resource_listdir')
def test_get_lang_choices(listdir_mock, listdir_value, expected_result, koles_checker):
    """Test that proper language names are fetched from the resources."""
    listdir_mock.return_value = listdir_value

    assert koles_checker._get_lang_choices() == expected_result
