import json
from enum import Enum

import requests

from fakenews_detector.url_utils import get_data_path


def append_if_exists(_json, _list, key):
    str_info = _json[key]
    if str_info is not '':
        _list.append(str_info)


class NewsVerdict(Enum):
    FAKE = 'Fake'
    REAL = 'Real'
    WARNING = 'Warning'
    UNKNOWN = 'Unknown'


class AbstractInfo:
    # TODO - add description
    def get_info(self):
        raise NotImplementedError

    def get_verdict(self, category):
        raise NotImplementedError

    @staticmethod
    def check(domain, sources):
        raise NotImplementedError

    @staticmethod
    def print_info(verdicts, categories, descriptions, source_notes):
        str_result = ''
        for i, verdict in enumerate(verdicts):
            str_result += 'Verdict' + str(i + 1) + ': ' + verdict.value + '\n'
            str_result += '\tCategory: ' + categories[i] + '\n'
            str_result += '\tDescription: ' + descriptions[i] + '\n'
        for i, note in enumerate(source_notes):
            str_result += 'Source note' + str(i + 1) + ': ' + note + '\n'
        return str_result


class OpenSourcesInfo(AbstractInfo):
    """
    Class containing tags and information about specific domain with fake news based on 
    http://www.opensources.co/ database
    """

    def __init__(self, domain, categories, source_notes):
        self.domain = domain
        self.categories = categories
        self.source_notes = source_notes

    @staticmethod
    def init_categories_descriptions():
        with open(get_data_path('opensources/tags.json')) as data_file:
            return json.load(data_file)

    categories_descriptions = init_categories_descriptions.__func__()

    def get_verdict(self, category):
        return {
            'fake': NewsVerdict.FAKE,
            'satire': NewsVerdict.WARNING,
            'bias': NewsVerdict.FAKE,
            'conspiracy': NewsVerdict.FAKE,
            'rumor': NewsVerdict.FAKE,
            'state': NewsVerdict.WARNING,
            'junksci': NewsVerdict.FAKE,
            'hate': NewsVerdict.WARNING,
            'clickbait': NewsVerdict.WARNING,
            'unreliable': NewsVerdict.WARNING,
            'political': NewsVerdict.WARNING,
            'reliable': NewsVerdict.REAL
        }[category]

    def get_info(self):
        verdicts = [self.get_verdict(x) for x in self.categories]
        categories = self.categories
        descriptions = [self.categories_descriptions[x] for x in self.categories]
        source_notes = self.source_notes
        return verdicts, categories, descriptions, source_notes

    @staticmethod
    def check(domain, json_sources):
        json_domain_info = json_sources[domain]

        types_list = []
        append_if_exists(json_domain_info, types_list, 'type')
        append_if_exists(json_domain_info, types_list, '2nd type')
        append_if_exists(json_domain_info, types_list, '3rd type')

        notes_list = []
        append_if_exists(json_domain_info, notes_list, 'Source Notes (things to know?)')

        open_source_info = OpenSourcesInfo(domain=domain,
                                           categories=types_list,
                                           source_notes=notes_list)
        return open_source_info.get_info()


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
        with open(get_data_path('categories.json')) as data_file:
            return json.load(data_file)

    tags_descriptions = init_categories_descriptions.__func__()

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


def check_domain(domain, result):
    result += '#####################################################' + '\n'
    result += 'Checking domain: ' + domain + '\n'

    # Opensource
    result += 'Opensource check:' + '\n'
    json_opensource_data = requests.get(
        'https://raw.githubusercontent.com/BigMcLargeHuge/opensources/master/sources/sources.json').json()
    if domain.lower() in json_opensource_data.keys():
        result += AbstractInfo.print_info(*OpenSourcesInfo.check(domain=domain,
                                                                 json_sources=json_opensource_data))
    else:
        result += 'opensource_check: no information' + '\n'

    # Manualy added
    result += '\nManualy added check:' + '\n'
    with open(get_data_path('manualy_added_sites.json')) as data_file:
        json_manual_data = json.load(data_file)
    if domain.lower() in json_manual_data.keys():
        result += AbstractInfo.print_info(*OpenSourcesInfo.check(domain=domain,
                                                                 json_sources=json_manual_data))
    else:
        result += 'Manualy added: no information' + '\n'

    # Fakenews
    result += '\nFake news check:' + '\n'
    fakenews_result = fakenews_check(domain)
    if fakenews_result is not None:
        result += fakenews_result
    else:
        result += 'fakenews_check: no information' + '\n'
        result += '\n\n'
    return result
