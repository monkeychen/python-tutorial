import urllib.request
import urllib.parse

def download1(url):
    """Simple downloader"""
    return urllib.request.urlopen(url).read()


def download2(url):
    """Download function that catches errors"""
    print('Downloading:%s' % url)
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.request.URLError as e:
        print('Download error:%s' % e.reason)
        html = None
    return html


def download3(url, num_retries=2):
    """Download function that also retries 5XX errors"""
    print('Downloading:%s' % url)
    try:
        html = urllib.request.urlopen(url).read()
    except urllib.request.URLError as e:
        print('Download error:%s' % e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download3(url, num_retries - 1)
    return html


def download4(url, user_agent='wswp', num_retries=2):
    """Download function that includes user agent support"""
    print('Downloading:%s' % url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(request).read()
    except urllib.request.URLError as e:
        print('Download error:%s' % e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download4(url, user_agent, num_retries - 1)
    return html


def download5(url, user_agent='wswp', proxy=None, num_retries=2):
    """Download function with support for proxies"""
    print('Downloading:%s' % url)
    headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener()
    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
    except urllib.request.URLError as e:
        print('Download error:%s' % e.reason)
        html = None
        if num_retries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download5(url, user_agent, proxy, num_retries - 1)
    return html


download = download5


if __name__ == '__main__':
    # print(download('http://example.webscraping.com'))
    print(download('http://simiam.com'))
