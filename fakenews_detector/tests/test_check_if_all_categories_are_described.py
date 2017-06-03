from unittest import TestCase
import requests
from fakenews_detector.url_utils import get_data_path
import json


class TestDomainChecker(TestCase):

    @staticmethod
    def check_if_all_categories_are_described(json_data, json_categories):
        not_listed = []
        result = True
        for json_site in json_data:
            if json_site['siteCategory'] not in '' and json_site['siteCategory'] not in json_categories:
                not_listed.append(json_site)
                result = False
        if not result:
            print('Unknown categories (not described categories)')
            for site in not_listed:
                print(site['siteCategory'])
        return result

    def test_check_if_all_categories_are_described(self):
        json_data = requests.get(
            'https://raw.githubusercontent.com/aligajani/fake-news-detector/master/output/fake-news-source.json').json()

        with open(get_data_path('categories.json')) as data_file:
            json_categories = json.load(data_file)
        self.assertTrue(self.check_if_all_categories_are_described(json_data=json_data,
                                                                json_categories=json_categories))

