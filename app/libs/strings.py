"""
libs.strings

By default, uses `en-gb.json` file inside the `strings` top-level folder.

If language changes, set `libs.strings.default_locale` and run `libs.strings.refresh()`
"""
import json

default_locale = "en-gb"
cached_strings = {}


def refresh():
    """
    loads the file set in `strings` top-level folder using the default_locale variable and sets the value
    and key in cached_strings as a dictionary
    :return
    """
    global cached_strings
    with open(f"../libs/strings/{default_locale}.json") as f:
        cached_strings = json.load(f)


def get_text(name: str) -> str:
    """
    get the text in the the cached strings by the name
    :param name: the name index passed as a key to cached_strings
    :return:
        value from the key hash table got from the name as key
    :rtype:
        String
    """
    return cached_strings[name]


def set_default_locale(locale):
    """
    change the default locale to another locale
    :param locale: the locale t change to eg: en-us or es-es
    :return:
    """
    global default_locale
    default_locale = locale


refresh()
