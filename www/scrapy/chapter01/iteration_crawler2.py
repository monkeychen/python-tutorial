import itertools
from common import download


def iteration():
    # maximum number of consecutive download errors allowed
    max_errors = 5
    # current number of consecutive download errors
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-{}'.format(page)
        html = download(url)
        if html is None:
            # received an error trying to download this webpage
            num_errors += 1
            if num_errors == max_errors:
                # reached maximum amount of errors in a row so exit
                break
            # so assume have reached the last country ID and can stop downloading
        else:
            # success - can scrape the result
            # ...
            num_errors = 0


if __name__ == '__main__':
    iteration()
