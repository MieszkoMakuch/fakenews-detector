from setuptools import setup

# Command to update package python setup.py sdist upload -r pypi

setup(
    name='fakenews_detector',
    packages=['fakenews_detector', 'fakenews_detector.fake_fact_ai'],
    version='0.1.24',
    description='Detect fake and get information about the source.',
    author='Mieszko Makuch',
    author_email='mmakuch@googlemail.com',
    url='https://github.com/',
    download_url='https://mieszko_makuch@bitbucket.org/mieszko_makuch/fakenews_detector.git',
    keywords=['fakenews', 'fake', 'news', 'detector'],
    package_data={'fakenews_detector': ['json_local/*', 'json_local/opensources/*', 'fake_fact_ai/static/*']},
    zip_safe=False,
    install_requires=[
        "validators==0.11.3",
        "numpy==1.11.3",
        "scipy==0.18.1",
        "sklearn==0.0",
        "nltk==3.2.4"
    ]
)
