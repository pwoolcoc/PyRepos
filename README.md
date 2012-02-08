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

There are a few configuration options, mostly just flags.
The one required argument is `repos_dir`, which gives the program a
starting place to look for repositories.

You can set all of the options in your config file(s), using standard
sh syntax.  You can specify the  in your config file(s) by using `flag=true`
or `flag=false`.  You can also specify the flags on the command line, which
will override any settings in your config files.  You specify the flags
on the command line by using `--flag` or `--no-flag`.  Here are the
available options:

    --silent
    --no-silent

    This option, if set, keeps the header and table headings from
    printing out


    --full-path
    --no-full-path

    This option, if set, changes the default way paths are printed from
    relative paths into full paths


    --dirty
    --no-dirty

    This option, if set, only selects repos that are currently dirty

The example config can be found in `pyrepos.config.example`, and the
program looks for config files in the following files, in this order:

  1. /etc/pyrepos
  2. ~/.pyrepos
  3. ~/.config/pyrepos

