from distutils.core import setup

setup(
    name='fakenews_detector',
    packages=['fakenews_detector'],
    version='0.1.1',
    description='Detect fake and get information about the source.',
    author='Mieszko Makuch',
    author_email='mmakuch@googlemail.com',
    url='https://github.com/',
    download_url='https://mieszko_makuch@bitbucket.org/mieszko_makuch/fakenews_detector.git',
    keywords=['fakenews', 'fake', 'news', 'detector'],
    classifiers=[],
    package_data={'fakenews_detector': ['json_local/*']},
)
