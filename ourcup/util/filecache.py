import hashlib
import os
import codecs
import logging

"""
Super basic file-based cache (utf-8 friendly).  Helpful if you're developing a 
webpage scraper and want to be a bit more polite to the server you're scraping 
while developing. The idea is that it caches content in files, each named by the 
key you pass in (use the md5_key helper to generate keys and make this super easy).
"""

DEFAULT_DIR = "cache"

cache_dir = DEFAULT_DIR

logger = logging.getLogger(__name__)


def md5_key(string):
    """
    Use this to generate filenae keys
    """
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def set_dir(new_dir=DEFAULT_DIR):
    """
    Don't need to call this, unless you want to override the default location
    """
    global cache_dir
    cache_dir = new_dir
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    logger.info("Caching files to {}".format(cache_dir))


def contains(key):
    """
    Returns true if a file named by key is in the cache dir
    """
    global cache_dir
    return os.path.isfile(os.path.join(cache_dir, key))


def get(key):
    """
    Returns the contents of the file named by key from the cache dir.
    Returns None if file doesn't exist
    """
    global cache_dir
    if os.path.isfile(os.path.join(cache_dir, key)):
        with codecs.open(os.path.join(cache_dir, key), mode="r", encoding='utf-8') as myfile:
            return myfile.read()
    return None


def put(key, content):
    """
    Creates a file in the cache dir named by key, with the content in it
    """
    global cache_dir
    logger.debug("caching {} in {}".format(key, cache_dir))
    logger.debug("  {}".format(content))
    text_file = codecs.open(os.path.join(cache_dir, key), encoding='utf-8', mode="w")
    text_file.write(content.decode('utf-8'))
    text_file.close()
