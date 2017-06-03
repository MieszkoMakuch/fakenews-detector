import sys
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')  # bdist_wininst
    sys.exit()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='fakenews_detector',
    packages=['fakenews_detector'],
    version='0.1.7',
    description='Detect fake and get information about the source.',
    author='Mieszko Makuch',
    author_email='mmakuch@googlemail.com',
    url='https://github.com/',
    download_url='https://mieszko_makuch@bitbucket.org/mieszko_makuch/fakenews_detector.git',
    keywords=['fakenews', 'fake', 'news', 'detector'],
    classifiers=[],
    package_data={'fakenews_detector': ['json_local/*', 'json_local/opensources/*']},
    include_package_data=True,
    install_requires=required,
    zip_safe=False
)
