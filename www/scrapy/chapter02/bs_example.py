import urllib.request as urllib2
from bs4 import BeautifulSoup

def scrape(html):
    soup = BeautifulSoup(html, 'lxml')
    # locate the area row
    tr = soup.find(attrs={'id': 'places_area__row'})
    # 'class' is a special python attribute so instead 'class_' is used
    # locate the area tag
    td = tr.find(attrs={'class': 'w2p_fw'})
    area = td.text  # extract the area contents from this tag
    return area

if __name__ == '__main__':
    html = urllib2.urlopen('http://example.webscraping.com/places/default/view/United-Kingdom-239').read().decode('utf-8')
    print(scrape(html))
