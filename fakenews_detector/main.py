import json
from urllib.parse import ParseResult
from urllib.parse import urlparse

import requests
import validators

valid_urls = ['http://www.google.pl/',
              'google.pl/',
              'google.pl',
              'www.google.pl/',
              'http://google.pl/',
              'https://www.google.pl/']

not_valid_urls = ['http://www.']


def format_url(url):
    """
    Formats url by adding 'http://' if necessary and deleting 'www.' 
    e.g. the following urls: 
    'http://www.google.pl/', 'google.pl/', 'google.pl', 'www.google.pl/', 'http://google.pl/', 'https://www.google.pl/'
    will be all formatted to: http://google.pl/
    """
    parsed_url = urlparse(url, 'http')
    netloc = parsed_url.netloc or parsed_url.path
    path = parsed_url.path if parsed_url.netloc else ''
    netloc = netloc.replace('www.', '')

    parsed_url = ParseResult('http', netloc, path, *parsed_url[3:])
    if not validators.url(parsed_url.geturl()):
        raise ValueError('Provided url=' + url + ' is not valid')
    return parsed_url.geturl()


def get_domain(url):
    return urlparse(format_url(url)).hostname


class OpenSourcesInfo:
    """
    Class containing tags and information about specific domain with fake news based on http://www.opensources.co/ database
    """

    def __init__(self, domain, categories, source_notes):
        self.domain = domain
        self.categories = categories
        self.source_notes = source_notes

    @staticmethod
    def init_tags_descriptions():
        with open('json_local/opensources/tags.json') as data_file:
            return json.load(data_file)

    tags_descriptions = init_tags_descriptions.__func__()

    def print_info(self):
        print('Domain: ' + self.domain)
        for i, category in enumerate(self.categories):
            print("Category" + str(i + 1) + ": " + self.tags_descriptions[category])
        for i, note in enumerate(self.source_notes):
            print("Source note " + str(i + 1) + ": " + note)

    def string_info(self):
        result = ''
        result += 'Domain: ' + self.domain + '\n'
        for i, category in enumerate(self.categories):
            result += "Category" + str(i + 1) + ": " + self.tags_descriptions[category] + '\n'
        for i, note in enumerate(self.source_notes):
            result += "Source note " + str(i + 1) + ": " + note + '\n'
        return result


def append_if_exists(_json, _list, key):
    str_info = _json[key]
    if str_info is not '':
        _list.append(str_info)


def opensource_check(domain):
    json_data = requests.get(
        'https://raw.githubusercontent.com/BigMcLargeHuge/opensources/master/sources/sources.json').json()
    if domain.lower() in json_data.keys():
        json_domain_info = json_data[domain]

        types_list = []
        append_if_exists(json_domain_info, types_list, 'type')
        append_if_exists(json_domain_info, types_list, '2nd type')
        append_if_exists(json_domain_info, types_list, '3rd type')

        notes_list = []
        append_if_exists(json_domain_info, notes_list, 'Source Notes (things to know?)')

        open_source_info = OpenSourcesInfo(domain=domain,
                                           categories=types_list,
                                           source_notes=notes_list)
        return open_source_info.string_info()
    return None

class FakeNewsDBInfo:
    """
    Class containing tags and information about specific domain with fake news based on the following google sheet:
    https://docs.google.com/spreadsheets/d/1xDDmbr54qzzG8wUrRdxQl_C1dixJSIYqQUaXVZBqsJs/edit#gid=1337422806
    """

    def __init__(self, domain, name, categories, political_alignments, source_notes):
        self.domain = domain
        self.name = name
        self.categories = categories
        self.political_alignments = political_alignments
        self.source_notes = source_notes

    @staticmethod
    def init_categories_descriptions():
        with open('json_local/categories.json') as data_file:
            return json.load(data_file)

    tags_descriptions = init_categories_descriptions.__func__()

    def print_info(self):
        print('Domain: ' + self.domain)
        for i, type in enumerate(self.categories):
            print("Category" + str(i + 1) + ": " + self.tags_descriptions[type])
        for i, note in enumerate(self.source_notes):
            print("Source note " + str(i + 1) + ": " + note)

    def string_info(self):
        result = ''
        result += 'Domain: ' + self.domain + '\n'
        for i, type in enumerate(self.categories):
            result += "Category" + str(i + 1) + ": " + self.tags_descriptions[type] + '\n'
        for i, note in enumerate(self.source_notes):
            result += "Source note " + str(i + 1) + ": " + note + '\n'
        return result


def fakenews_check(domain):
    json_data = requests.get(
        'https://raw.githubusercontent.com/aligajani/fake-news-detector/master/output/fake-news-source.json').json()
    for json_site in json_data:
        if domain.lower() in json_site['siteUrl'].lower():
            name = json_site['siteTitle']

            categories_list = []
            append_if_exists(json_site, categories_list, 'siteCategory')

            political_alignments_list = []
            append_if_exists(json_site, political_alignments_list, 'sitePoliticalAlignment')

            source_notes_list = []
            append_if_exists(json_site, source_notes_list, 'siteNotes')

            fakenews_db_info = FakeNewsDBInfo(domain=domain,
                                              name=name,
                                              categories=categories_list,
                                              political_alignments=political_alignments_list,
                                              source_notes=source_notes_list)
            return fakenews_db_info.string_info()
    return None


def check_news(domain):
    result = ''
    result += '#####################################################' + '\n'
    result += 'Checking domain: ' + domain + '\n'
    result += 'Opensource check:' + '\n'

    open_source_result = opensource_check(domain)
    if open_source_result is not None:
        result += open_source_result
    else:
        result += 'opensource_check: no information' + '\n'
    result += '\nFake news check:' + '\n'

    fakenews_result = fakenews_check(domain)
    if fakenews_result is not None:
        result += fakenews_result
    else:
        result +='fakenews_check: no information' + '\n'
        result += '\n\n'

    return result


def check_if_all_categories_are_described():
    json_data = requests.get(
        'https://raw.githubusercontent.com/aligajani/fake-news-detector/master/output/fake-news-source.json').json()

    with open('json_local/categories.json') as data_file:
        json_tags = json.load(data_file)

    not_listed = []
    for json_site in json_data:
        if json_site['siteCategory'] not in json_tags:
            not_listed.append(json_site)
    for site in not_listed:
        print(site['siteCategory'])

# opensource_check test
domain_aheadoftheherd = get_domain('aheadoftheherd.com')
print(check_news(domain_aheadoftheherd))

domain_mediamass = get_domain('http://en.mediamass.net/')
print(check_news(domain_mediamass))

domain_100PercentFedUp = get_domain('100PercentFedUp.com')
check_news(domain_100PercentFedUp)