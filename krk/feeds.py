"""
Managing feeds

"""
from datetime import datetime

from pytz import UTC

from krk.config import db


def add_feed(feed_name, feed_url, interval):
    """
    Add a new feed

    :param feed_name: This will be the id of the feed.
    :param feed_url: URL of the feed
    :param interval: In seconds, interval between each poll of the feed.
    """

    if db["feeds"].find_one({"_id": feed_name}):
        raise Exception("Duplicated id")
    else:
        db["feeds"].insert_one({
            "_id": feed_name,
            "url": feed_url,
            "interval": interval,
            "pollTime": datetime.now(tz=UTC)
        })
