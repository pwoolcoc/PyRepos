#!/usr/bin/python

from __future__ import print_function

import argparse
from functools import partial
import os
from git.repo.base import Repo
from git.repo.fun import is_git_dir
from git.exc import InvalidGitRepositoryError


REPOS_DIR = os.path.join(os.path.expanduser(u"~pwoolcoc"), u"Dropbox", u"repos")

RESET = u"\033[0m"
RED = u"\033[1;31m"
GREEN = u"\033[1;32m"
BLUE = u"\033[1;34m"

YES = u"{green}Yes{reset}".format(green=GREEN, reset=RESET)
NO = u"{red}No{reset}".format(red=RED, reset=RESET)
PATH = u"{blue}{heading}{reset}"

def import_settings():
    user_dir = os.expanduser("~")
    files = ['/etc/pyrepos',
             os.path.join(user_dir, '.pyrepos')
             os.path.join(user_dir, '.config', 'pyrepos')]
    settings = {}
    for file_ in files:
        settings = get_pairs(file_, settings)

def get_pairs(src, settings):
    if os.path.exists(src):
        with open(src) as f:
            for line in f:
                line = line.strip()
                if not line.startswith("#"):
                    key, value = (x.strip() for x in line.split("="))
                    settings.update(key=value)
    return settings

def search(path, search_string):
    if search_string is None or search_string.lower() in path.lower():
        return True
    return False

def main(repo_str=None, repos_dir=REPOS_DIR):
    print("\nRepository Directory: {repos_dir}\n".format(repos_dir=repos_dir))
    print("{repos:<60} {bare}".format(repos="Repositories", bare="Bare?"))
    print("{0:-^70}".format(""))

    do_search = partial(search, search_string=repo_str)

    for path, dirs, files in os.walk(repos_dir):
        try:
            repo = Repo(path)
            if is_git_dir(path) and do_search(path):
                path = PATH.format(blue=BLUE,
                                   heading=os.path.relpath(path, repos_dir),
                                   reset=RESET)
                bare = YES if repo.bare else NO
                print("{path:_<70} {bare}".format(path=path, bare=bare))
        except InvalidGitRepositoryError, NoSuchPathError:
            pass

    print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="List available git repositories.\nDefault repository dir is:\n\n{0}".format(REPOS_DIR))
    parser.add_argument(u"-s", u"--search", help=u"Optional search string",
            dest="search_string", default=None)
    parser.add_argument(u"--repository-dir", help=u"Optional top-level repository directory",
            dest="repository_dir", default=REPOS_DIR)
    args = parser.parse_args()
    main(args.search_string, args.repository_dir)


