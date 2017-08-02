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


@c.task(name="krk.download")
def download(url, filename=None, params=None, headers=HEADERS):
    """
    Get and download an url into a file
    
    :param str url: url to download
    :param path filename: Path to save the result file 
    :param dict params: parameters to pass to requests
    :param dict headers: headers to pass to requests
    :return: url and the path downloaded
    :rtype: (str, str)
    """
    l.info("Task getting url %s", url)
    r = get(url, params=params, headers=headers)

    file_type = ".json" if isinstance(r, dict) else ".result"

    if not filename:
        up = urlparse(url)
        domain = up.netloc
        filename = "{}_{}{}".format(domain, to_b32(int(time.time())), file_type)

    path = os.path.join(filename)

    return url, write_file(r, path)


@c.task(name="krk.enq-feed")
def enq(feed_id, interval):
    """
    Enqueue the feed to be download

    :param str feed_id: Id of the feed to enqueue
    :param interval: How long after the download are enqueued the feed should be poll again?
    """

    feed = db["feeds"].find_one({"_id": feed_id})

    l.debug("Enqueueing %s", feed_id)

    filename = "{}_{}.feed".format(feed_id, to_b32(int(time.time())))

    # Block here so that we have the path. This change the nature of next_poll date
    url, path = download(feed["url"], filename=filename)

    poll_attempt = {
        "path": path,
        "time": datetime.now(tz=UTC)
    }

    next_poll = poll_attempt["time"] + timedelta(seconds=interval)

    db["feeds"].update_one({"_id": feed_id}, {"$set": {"pollTime": next_poll}, "$push": {"pollAttempts": poll_attempt}})
    return


if __name__ == '__main__':
    pass
