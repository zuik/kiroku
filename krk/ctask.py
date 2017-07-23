"""
Wrapper for various thing from celery
"""
import logging
from urllib.parse import urlparse

import os
import time

from krk import YEAR_2017

from krk.config import c, HEADERS, db
from krk.gen_id import to_b32
from krk.requester import get
from krk.tools import write_file

l = logging.getLogger(__name__)


@c.task(name="download")
def download(url, filename=None, params=None, headers=HEADERS, filetype=None):
    """
    Get and download an url into a file
    
    :param str url: 
    :param path filename: Path to save the result file 
    :param dict params: 
    :param dict headers: 
    :return: 
    """
    l.info("Task getting url %s", url)
    r = get(url, params=params, headers=headers)

    if not filetype:
        filetype = ".json" if isinstance(r, dict) else ".result"

    if not filename:
        up = urlparse(url)
        domain = up.netloc
        filename = "{}_{}{}".format(domain, to_b32(int(time.time() - YEAR_2017)), filetype)

    path = os.path.join(filename)

    return write_file(r, path)


if __name__ == '__main__':
    download("http://bls.org")
