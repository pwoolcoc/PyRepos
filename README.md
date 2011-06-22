# PyRepos

### Small tool to find and show code repositories on your filesystem

Like a lot of developers, I have a lot of code repositories to keep
track of.  I use Dropbox to backup my bare git repos, and sometimes I
forget exactly where a repository is kept in the directory structure.
This tool looks for code repos, and displays their locations, along with
other details.

Right now it only supports Git repos, but I want it to be able to show
hg/bzr/svn repos as well.

### Configuration

There isn't really a lot of configuration, right now the only option
available is `repos_dir`, which lets you set a default location under
which repositories are kept.  That saves you a little typing if you
usually keep your repositories in one gigantic directory tree (like
me...).  The example config can be found in `pyrepos.config.example`,
and the program looks for config files in the following files, in this
order:

  - /etc/pyrepos
  - ~/.pyrepos
  - ~/.config/pyrepos

