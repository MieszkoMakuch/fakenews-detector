from fakenews_detector.main import check_news, info_to_str

url_100PercentFedUp = 'http://100percentfedup.com/comedian-kathy-griffins-7th-final-venue-cancelswhos-laughing-now/'
print(info_to_str(check_news(url_100PercentFedUp)))

url_ancientcode = 'http://www.ancient-code.com/does-this-top-secret-memo-finally-prove-ufo-crash-roswell/'
print(info_to_str(check_news(url_ancientcode)))

url_szdziennik = 'http://aszdziennik.pl/120211,akcja-fanow-na-koncercie-kings-of-leon-w-czasie-use-somebody-odloza-smartfony-i-popatrza-na-scene'
print(info_to_str(check_news(url_szdziennik)))

url_onet = 'http://muzyka.onet.pl/wywiady/margaret-dzis-popelniam-bledy-z-podniesiona-glowa-wywiad/s7c0bq'
print(info_to_str(check_news(url_onet)))

url_test = 'sfgate.com'
print(info_to_str(check_news(url_test)))