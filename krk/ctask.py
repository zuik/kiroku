"""
Wrapper for various thing from celery
"""
import logging
import time
from datetime import datetime, timedelta
from urllib.parse import urlparse

import os
from pytz import UTC

from krk.gen_id import to_b32

from krk.config import c, HEADERS, db
from krk.requester import get
from krk.tools import write_file

l = logging.getLogger(__name__)


@c.task(name="download")
def download(url, filename=None, params=None, headers=HEADERS, filetype=None):
    """
    Get and download an url into a file
    
    :param filetype:
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
        filename = "{}_{}{}".format(domain, to_b32(int(time.time())), filetype)

    path = os.path.join(filename)

    return write_file(r, path)


@c.task(name="enq-feed")
def enq(feed_id, interval):
    feed = db["feeds"].find_one({"_id": feed_id})

    l.debug("Enqueueing %s", feed_id)

    filename = "{}_{}.feed".format(feed_id, to_b32(int(time.time())))

    download.delay(feed["url"], filename=filename)

    next_poll = datetime.now(tz=UTC) + timedelta(seconds=interval)

    db["feeds"].update_one({"_id": feed_id}, {"$set": {"pollTime": next_poll}})
    return


if __name__ == '__main__':
    pass
