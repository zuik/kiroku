import logging

import requests

from krk.config import HEADERS

l = logging.getLogger(__name__)


def get(url, params=None, headers=HEADERS):
    """
    Issue a GET request and return the response

    :return: <dict> JSON parsed from the response
    """
    l.info("Getting %s", url)
    r = requests.get(url, params=params, headers=headers)
    if r.status_code == 200:
        try:
            l.debug("Got JSON from url %s, returning", url)
            return r.json()
        except:
            l.debug("Not JSON from url %s, returning", url)
            # Do not let requests to handle text encoding.
            return r.content
    else:
        l.error("Request error. Status code %d from url %s", r.status_code, url)
        raise Exception("Request error", "Status code: {}".format(r.status_code))
