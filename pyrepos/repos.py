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
from git.exc import InvalidGitRepositoryError, NoSuchPathError


YES = u"Yes"
NO = u"No"
PATH = u"{heading}"
DEFAULT_DIR = u"/"

def get_settings(cmd_line_opts, files=None):
    if files is None:
        user_dir = os.path.expanduser("~")
        files = ['/etc/pyrepos',
                 os.path.join(user_dir, '.pyrepos'),
                 os.path.join(user_dir, '.config', 'pyrepos')]
    settings = {}
    for file_ in files:
        settings.update(**get_pairs(file_))
    for opt in cmd_line_opts:
        val = cmd_line_opts.get(opt)
        if val is not None:
            settings.update({opt: cmd_line_opts.get(opt)})
    return settings

def get_pairs(src):
    _settings = {}
    if os.path.exists(src):
        with open(src) as f:
            commands = shlex.split(f.read(), comments=True)
            for item in commands:
                key, value = item.split("=")
                _settings.update({key: value})
    return _settings

def main():
    arguments = parse_args()
    settings = get_settings(arguments)
    repos_dir = settings.get('repos_dir', DEFAULT_DIR)
    repos_dir = os.path.realpath(repos_dir)

    if arguments.get('dir', False):
        print(repos_dir)
    else:
        print_results(repos_dir, settings)



def get_results(repos_dir):
    paths = []
    for path, dirs, files in os.walk(repos_dir):
        if is_git_dir(path):
            repo = Repo(path)
            path = PATH.format(heading=os.path.relpath(path, repos_dir))
            bare = YES if repo.bare else NO
            dirty = YES if repo.is_dirty() else NO
            paths.append({'path': path, 'bare': bare, 'dirty': dirty})
    return paths


def print_results(repos_dir, settings):
    results = get_results(repos_dir)
    lens = [len(entry['path']) for entry in results]
    max_len = max(lens + [12])


    if not settings.get('silent', False):
        print("\nBase Directory: {repos_dir}\n".format(repos_dir=repos_dir))
        print("{repos:<{width}}\t{bare:<8}\t{dirty}".format(repos="REPOSITORIES",
                bare="BARE", dirty="DIRTY", width=max_len))

    for entry in results:
        print("{path:<{width}}\t{bare:<8}\t{dirty}".format(path=entry['path'],
                                                           bare=entry['bare'],
                                                           dirty=entry['dirty'],
                                                           width=max_len))

    print()

def parse_args():
    if _argparse:
        parser = argparse.ArgumentParser(
                description="List available git/hg/bzr/svn repositories.")
        parser.add_argument(u"repos_dir", nargs="?", default=None,
                help="Directory to search in. Defaults to repos_dir in ~/.pyrepos")
        parser.add_argument(u"--dir", action="store_true")
        parser.add_argument(u'--silent', action="store_true")
        args = parser.parse_args()
    else:
        parser = optparse.OptionParser()
        parser.add_option(u'repos_dir', default=None)
        parser.add_option(u'--dir', action=u'store_true')
        parser.add_option(u'--silent', action=u'store_true')
        options, args = parser.parse_args()
    return vars(args)

if __name__ == "__main__":
    pass


