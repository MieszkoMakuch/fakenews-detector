import json
from unittest import TestCase

from fakenews_detector.domain_checker import OpenSourcesInfo
from fakenews_detector.news_info import NewsVerdict
from fakenews_detector.url_utils import get_data_path


class TestCheckNews(TestCase):
    def test_check_news(self):
        # Check Manually added
        with open(get_data_path('manualy_added_sites.json')) as data_file:
            json_manual_data = json.load(data_file)

        # washingtonpost.com verdict should be credible
        domain_washington_post = 'washingtonpost.com'
        if OpenSourcesInfo.can_check_url(domain_washington_post, json_manual_data):
            verdict, _, _, _ = OpenSourcesInfo.check(domain=domain_washington_post, json_sources=json_manual_data)
            assert verdict[0] == NewsVerdict.REAL
        else:
            self.fail('Cannot check ' + domain_washington_post)

        # ancient-code.com verdict should be fake
        domain_washington_post = 'ancient-code.com'
        if OpenSourcesInfo.can_check_url(domain_washington_post, json_manual_data):
            verdict, _, _, _ = OpenSourcesInfo.check(domain=domain_washington_post, json_sources=json_manual_data)
            assert verdict[0] == NewsVerdict.FAKE
        else:
            self.fail('Cannot check ' + domain_washington_post)

        # chaser.com.au verdict should be warning
        domain_washington_post = 'chaser.com.au'
        if OpenSourcesInfo.can_check_url(domain_washington_post, json_manual_data):
            verdict, _, _, _ = OpenSourcesInfo.check(domain=domain_washington_post, json_sources=json_manual_data)
            assert verdict[0] == NewsVerdict.WARNING
        else:
            self.fail('Cannot check ' + domain_washington_post)
