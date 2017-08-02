"""
Managing feeds

"""
from datetime import datetime
from urllib.parse import urlparse

import random
from pytz import UTC

from krk.config import db
from krk.gen_id import to_b32


def add_feed(feed_url, interval, feed_name=None):
    """
    Add a new feed

    :param feed_name: This will be the id of the feed.
    :param feed_url: URL of the feed
    :param interval: In seconds, interval between each poll of the feed.
    """

    if not feed_name:
        # Automatically generated feed_id
        up = urlparse(feed_url)
        domain = up.netloc
        feed_name = f"{domain}_{to_b32(random.randint(1024))}"

    if db["feeds"].find_one({"_id": feed_name}):
        raise Exception("Duplicated id")
    else:
        db["feeds"].insert_one({
            "_id": feed_name,
            "url": feed_url,
            "interval": interval,
            "pollTime": datetime.now(tz=UTC)
        })


def feed_info(feed_name):
    pass
