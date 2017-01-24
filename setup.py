import os
from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


setup(
    name='cfgov',
    version_format='{tag}.dev{commitcount}+{gitsha}',
    author='CFPB',
    author_email='tech@cfpb.gov',
    maintainer='cfpb',
    maintainer_email='tech@cfpb.gov',
    packages= find_packages(where='./cfgov/'),
    package_dir={'':'cfgov'},
    include_package_data=True,
    description=u'django project powering consumerfinance.gov',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    long_description=read_file('README.md'),
    zip_safe=False,
    setup_requires=['cfgov-setup==1.2','setuptools-git-version'],
    frontend_build_script= 'frontend.sh',
)
