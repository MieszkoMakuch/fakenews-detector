from unittest import TestCase

from fakenews_detector.url_utils import format_url, get_domain


class TestUrlUtils(TestCase):
    valid_urls_google_pl = ['http://www.google.pl/',
                            'google.pl/',
                            'google.pl/',
                            'www.google.pl/',
                            'http://google.pl/',
                            'https://www.google.pl/']

    not_valid_urls = ['http://www.', 'http://google.']

    def test_format_url(self):
        # Test valid urls
        expected_url = 'http://google.pl/'
        for url in self.valid_urls_google_pl:
            self.assertEqual(expected_url, format_url(url))

        # Test not valid urls
        for url in self.not_valid_urls:
            with self.assertRaises(ValueError):
                format_url(url)

    def test_get_domain(self):
        expected_domain = 'google.pl'
        for url in self.valid_urls_google_pl:
            self.assertEqual(expected_domain, get_domain(url))
