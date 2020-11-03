import urllib.request as urllib2
import re


def scrape(html):
    area = re.findall('<tr id="places_area__row">.*?<td\s*class=["\']w2p_fw["\']>(.*?)</td>', html)[0]
    return area


if __name__ == '__main__':
    html = urllib2.urlopen('http://example.webscraping.com/places/default/view/United-Kingdom-239').read().decode('utf-8')
    print(scrape(html))
