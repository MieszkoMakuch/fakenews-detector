# Fake news detector
Article and domain analyzer written in python 3 to help user detect fake news content.

## Online demo
View a working online demo here (it may take a few seconds to deploy):

#### [Online demo](https://protected-inlet-79294.herokuapp.com/)

#### [Demo - Github repository](https://github.com/MieszkoMakuch/fakenews-detector-demo)

### Try to paste this examples and see the results.
#### Analysis based on human maintained lists:
Fake, junk science:

`http://www.ancient-code.com/did-ancient-mankind-know-the-secrets-of-levitation/`

Warning, gossip:

`http://en.mediamass.net/people/colin-hanks/married.html`

Real, Credible:

`http://www.bbc.com/news/uk-40148737`

#### Analysis based on AI:
Fake:

`http://aszdziennik.pl/120211,akcja-fanow-na-koncercie-kings-of-leon-w-czasie-use-somebody-odloza-smartfony-i-popatrza-na-scene`

`http://dziennikbulwarowy.pl/146/straszyl-wiernych-przez-megafon.html#edytuj`

Real:

`http://wyborcza.pl/7,154903,21913047,liga-legii-mistrzostwo-zostaje-w-warszawie.html`

## Motivation
The Oxford Dictionaries Word of the Year 2016 was post-truth – an adjective defined as ‘relating to or denoting circumstances in which objective facts are less influential in shaping public opinion than appeals to emotion and personal belief’.

This program scrutinizes information available on the Internet, performs machine learning analysis and assists the user in verifying the credibility of the found information.

## Install
```bash
pip install fakenews_detector
```
Package installs successfully on macOS and heroku. However, you will run into some issues if you are trying to install on ubuntu.
## Usage example
You can find more usage examples in `examples/` folder, also as the jupyter notebook.

### Example: fake news detection
```python
from fakenews_detector.main import check_news, info_to_str

# Some page with fake news
url_100PercentFedUp = 'http://100percentfedup.com/comedian-kathy-griffins-7th-final-venue-cancelswhos-laughing-now/'

print(info_to_str(check_news(url_100PercentFedUp)))

```
Output:
```
Checking domain: 100percentfedup.com
Source: OpenSource http://www.opensources.co/
	Verdict1: Fake
		Category: bias
		Description: Extreme Bias - Sources that come from a particular point of view and may rely on propaganda, decontextualized information, and opinions distorted as facts.
Source: FakeNewsDB
	Verdict1: Warning
		Category: clickbait
		Description: Clickbait - Sources that provide generally credible content, but use exaggerated, misleading, or questionable headlines, social media descriptions, and/or images.
		Source note 1: Political alignment: right

```
### Example: credible source
```python
from fakenews_detector.main import check_news, info_to_str

# Credible source
url_bbc = 'http://www.bbc.com/news/uk-40148737'
print(info_to_str(check_news(url_bbc)))

```
Output:
```
Checking domain: bbc.com
Source: OpenSource http://www.opensources.co/
	Verdict1: Real
		Category: reliable
		Description: Credible - Sources that circulate news and information in a manner consistent with traditional and ethical practices in journalism (Remember: even credible sources sometimes rely on clickbait-style headlines or occasionally make mistakes. No news organization is perfect, which is why a healthy news diet consists of multiple sources of information).
Source: Artificial intelligence
	Verdict1: Real
		Category: Real News
		Description: Analysis performed by artificial intelligence indicate that this article is credible
		Source note 1: WARNING: This result may be inaccurate! This domain wasn't categorised on any human maintained list thus analysis was performed by machine learning module.


```