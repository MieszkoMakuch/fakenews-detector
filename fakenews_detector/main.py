import json

import requests
from newspaper import Article

from fakenews_detector.domain_checker import check_domain
from fakenews_detector.fake_fact_ai.application import mod
from fakenews_detector.url_utils import get_domain, get_data_path


def ai_check(article):
    predict_result = ''
    if article.title is not None:
        if mod.query(article.title) == 1:
            predict_result = "Real News"
        else:
            predict_result = "Fake News"
    return predict_result


def analyze_article(article, result):
    article.download()
    if not article.is_downloaded:
        raise ConnectionError('Cannot download the article')
    article.parse()
    result += 'AI check:' + '\n'
    result += ai_check(article) + '\n'
    return result


def check_news(url):
    # Get newspaper article
    article = Article(url)

    # Check domain
    domain = get_domain(url)
    result = ''
    result = check_domain(domain, result)

    # Analyze article

    # AI
    result += 'Analyzing article with ai:' + '\n'
    try:
        result = analyze_article(article, result)
    except ConnectionError as error:
        result += str(error)
    return result


def check_if_all_categories_are_described():
    json_data = requests.get(
        'https://raw.githubusercontent.com/aligajani/fake-news-detector/master/output/fake-news-source.json').json()

    with open(get_data_path('categories.json')) as data_file:
        json_tags = json.load(data_file)

    not_listed = []
    for json_site in json_data:
        if json_site['siteCategory'] not in json_tags:
            not_listed.append(json_site)
    for site in not_listed:
        print(site['siteCategory'])


url_ancientcode = 'http://www.ancient-code.com/does-this-top-secret-memo-finally-prove-ufo-crash-roswell/'
print(check_news(url_ancientcode))

url_100PercentFedUp = 'http://100percentfedup.com/comedian-kathy-griffins-7th-final-venue-cancelswhos-laughing-now/'
print(check_news(url_100PercentFedUp))

url_szdziennik = 'http://aszdziennik.pl/120211,akcja-fanow-na-koncercie-kings-of-leon-w-czasie-use-somebody-odloza-smartfony-i-popatrza-na-scene'
print(check_news(url_szdziennik))

url_onet = 'http://muzyka.onet.pl/wywiady/margaret-dzis-popelniam-bledy-z-podniesiona-glowa-wywiad/s7c0bq'
print(check_news(url_onet))
