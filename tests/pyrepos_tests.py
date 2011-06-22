from itertools import izip
from nose.tools import *
from unittest import TestCase

from pyrepos.repos import get_settings, get_pairs

TESTFILE = "./testfile"
ALTTESTFILE = "./alttestfile"

def make_one_config_file():
    with open(TESTFILE, "w") as f:
        f.write(u"name=Paul\n")

def make_two_config_files():
    files = [TESTFILE, ALTTESTFILE]
    contents = [
            {'name': "Paul", "age": "28"},
            {'name': "Bob"}
            ]
    for (file_, c) in izip(files, contents):
        _ = ["{0}={1}".format(k, c[k]) for k in c]
        to_write = "\n".join(_)
        with open(file_, "w") as f:
            f.write(to_write)


class PyReposTest(TestCase):
    def testGetPairs(self):
        """Get settings from one file"""
        make_one_config_file()
        s = get_pairs(TESTFILE)
        self.assertEqual({"name": "Paul"}, s)


    def testGetSettings(self):
        """Make sure we can get settings from files"""
        make_one_config_file()

        settings = get_settings([TESTFILE])
        self.assertEqual(settings, {'name': 'Paul'})

    def testGetSettingsMultipleFiles(self):
        """Ensures settings get overridden correctly"""
        make_two_config_files()

        settings = get_settings([TESTFILE, ALTTESTFILE])
        self.assertEqual(settings, {'name': "Bob", "age": "28"})
