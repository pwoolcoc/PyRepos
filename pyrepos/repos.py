#!/usr/bin/python

from __future__ import print_function

try:
    import argparse
    _argparse = True
except ImportError:
    import optparse
    _argparse = False

import os
import shlex

from git.repo.base import Repo
from git.repo.fun import is_git_dir


YES = u"Yes"
NO = u"No"
PATH = u"{heading}"
DEFAULT_DIR = u"/"
HOME = os.getenv("HOME")

def get_settings(cmd_line_opts, files=None):
    """
    Collects all settings, from files and the command line

    Returns a dict of settings
    """
    if files is None:
        files = ['/etc/pyrepos',
                 os.path.join(HOME, '.pyrepos'),
                 os.path.join(HOME, '.config', 'pyrepos')]
    settings = {}
    for file_ in files:
        settings.update(**get_pairs(file_))
    #print(settings)
    for opt in cmd_line_opts:
        val = cmd_line_opts.get(opt)
        if val is not None:
            settings.update({opt: cmd_line_opts.get(opt)})
    #print(settings)
    return settings

def get_pairs(src):
    _settings = {}
    if os.path.exists(src):
        with open(src) as f:
            commands = shlex.split(f.read(), comments=True)
            for item in commands:
                key, value = item.split("=")
                if value == u'true': value = True
                elif value == u'false': value = False
                _settings.update({key: value})
    return _settings

def main():
    arguments = parse_args()
    #print(arguments)
    settings = get_settings(arguments)
    #print(settings)
    repos_dir = settings.get('repos_dir', DEFAULT_DIR)
    repos_dir = os.path.realpath(repos_dir)

    if arguments.get('dir', False):
        print(repos_dir)
    else:
        print_results(repos_dir, settings)



def get_results(repos_dir, settings):
    paths = []
    collect_only_dirty = settings.get('dirty', False)
    show_full_path = settings.get('full_path', False)
    for path, dirs, files in os.walk(repos_dir):
        if is_git_dir(path):
            repo = Repo(path)
            path = os.path.dirname(path)
            if show_full_path:
                path = PATH.format(heading=os.path.join(repos_dir, path))
            else:
                path = PATH.format(heading=os.path.relpath(path, repos_dir))
            bare = repo.bare
            dirty = repo.is_dirty()
            if (collect_only_dirty and dirty) or (not collect_only_dirty):
                paths.append({'path': path, 'bare': bare, 'dirty': dirty})
    return paths


def print_results(repos_dir, settings):
    results = get_results(repos_dir, settings)
    lens = [len(entry['path']) for entry in results]
    max_len = max(lens + [12])


    if not settings.get('silent', False):
        print("\nBase Directory: {repos_dir}\n".format(repos_dir=repos_dir))
        print("{repos:<{width}}\t{bare:<8}\t{dirty}".format(repos="REPOSITORIES",
                bare="BARE", dirty="DIRTY", width=max_len))
        BARE = DIRTY = "Yes"
        NOT_BARE =  NOT_DIRTY = "No"
    else:
        BARE = "Bare"
        NOT_BARE = "Not Bare"
        DIRTY = "Dirty"
        NOT_DIRTY = "Not Dirty"

    for entry in results:
        is_dirty = DIRTY if entry.get('dirty') else NOT_DIRTY
        path = entry.get('path')
        is_bare = BARE if entry.get('bare') else NOT_BARE
        print("{path:<{width}}\t{bare:<8}\t{dirty}".format(path=path,
                                                           bare=is_bare,
                                                           dirty=is_dirty,
                                                           width=max_len))


def parse_args():
    if _argparse:
        parser = argparse.ArgumentParser(
                description="List available git/hg/bzr/svn repositories.")
        parser.add_argument(u"repos_dir", nargs="?", default=None)
        parser.add_argument(u"--dir", action=u"store_const", const=True)

        silent = parser.add_mutually_exclusive_group()
        silent.add_argument(u'--silent', default=None, dest="silent", action=u"store_true")
        silent.add_argument(u'--no-silent', default=None, dest="silent", action=u"store_false")

        dirty = parser.add_mutually_exclusive_group()
        dirty.add_argument(u'--dirty', default=None, dest=u'dirty', action=u"store_true")
        dirty.add_argument(u'--no-dirty', default=None, dest=u'dirty', action=u"store_false")

        full_path = parser.add_mutually_exclusive_group()
        full_path.add_argument(u'--full-path', default=None, dest=u'full_path', action=u'store_true')
        full_path.add_argument(u'--no-full-path', default=None, dest=u'full_path', action=u'store_false')

        args = parser.parse_args()
    else:
        parser = optparse.OptionParser()
        parser.add_option(u'repos_dir', default=None)
        parser.add_option(u'--dir', action=u'store_const', default=None, const=True)
        parser.add_option(u'--silent', action=u'store_const', default=None, const=True)
        parser.add_option(u'--dirty', action=u"store_const", default=None, const=True)
        parser.add_option(u'--full-path', action=u'store_const', default=None, const=True)
        parser.add_option(u'--no-silent', action=u"store_const", default=None, const=False)
        parser.add_option(u'--no-dirty', action=u"store_const", default=None, const=False)
        parser.add_option(u'--no-full-path', action=u'store_const', default=None, const=False)
        options, args = parser.parse_args()
    args = vars(args)
    return args

if __name__ == "__main__":
    pass


