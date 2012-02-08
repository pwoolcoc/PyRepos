try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

config = {
        'description': 'Tool to list git/hg/bzr/svn repositories in filesystem',
        'author': 'Paul Woolcock',
        'author_email': 'pwoolcoc@gmail.com',
        'version': '0.2',
        'install_requires': ['GitPython>=0.3.1'],
        'packages': find_packages(),
        'name': 'PyRepos',
        'url': 'https://github.com/pwoolcoc/PyRepos',
        'entry_points':{
            'console_scripts': [
                'repos = pyrepos.repos:main',
            ]
        },
        'test_suite': 'nose.collector',
        'tests_require': ['nose'],
}

setup(**config)

