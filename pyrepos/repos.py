#!/usr/bin/python

from __future__ import print_function

import argparse
import os
import shlex

from git.repo.base import Repo
from git.repo.fun import is_git_dir
from git.exc import InvalidGitRepositoryError, NoSuchPathError


RESET = u"\033[0m"
RED = u"\033[1;31m"
GREEN = u"\033[1;32m"
BLUE = u"\033[1;34m"

YES = u"{green}Yes{reset}".format(green=GREEN, reset=RESET)
NO = u"{red}No{reset}".format(red=RED, reset=RESET)
PATH = u"{blue}{heading}{reset}"

def get_settings(files=None):
    if files is None:
        user_dir = os.path.expanduser("~")
        files = ['/etc/pyrepos',
                 os.path.join(user_dir, '.pyrepos'),
                 os.path.join(user_dir, '.config', 'pyrepos')]
    settings = {}
    for file_ in files:
        settings.update(**get_pairs(file_))
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

def main(repos_dir=None):
    settings = get_settings()
    repos_dir = repos_dir or settings.get('repos_dir')
    assert repos_dir is not None
    repos_dir = os.path.realpath(repos_dir)
    print_results(repos_dir)


def print_results(repos_dir):
    print("\nRepository Directory: {repos_dir}\n".format(repos_dir=repos_dir))
    print("{repos:<60} {bare}".format(repos="Repositories", bare="Bare?"))
    print("{0:-^70}".format(""))

    for path, dirs, files in os.walk(repos_dir):
        try:
            repo = Repo(path)
            if is_git_dir(path):
                path = PATH.format(blue=BLUE,
                                   heading=os.path.relpath(path, repos_dir),
                                   reset=RESET)
                bare = YES if repo.bare else NO
                print("{path:_<70} {bare}".format(path=path, bare=bare))
        except (InvalidGitRepositoryError, NoSuchPathError):
            pass

    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="List available git/hg/bzr/svn repositories.")
    parser.add_argument(u"directory", nargs="?", default=None,
            help="Directory to search in. Defaults to repos_dir in ~/.pyrepos")
    args = parser.parse_args()
    main(args.directory)


