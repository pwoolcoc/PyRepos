try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

config = {
        'description': 'Tool to list git/hg/bzr/svn repositories in filesystem',
        'author': 'Paul Woolcock',
        'author_email': 'pwoolcoc@umflint.edu',
        'version': '0.1',
        'install_requires': ['GitPython==0.3.1'],
        'packages': find_packages(),
        'name': 'PyRepos',
        'entry_points':{
            'console_scripts': [
                'repos = listrepos.repos:main',
            ]
        },
}

setup(**config)

