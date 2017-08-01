"""
Poller for feeds

We will go through the database, and look at each, items and enqueue them accordingly.

For every feed in the database, we will store a corresponding status for the feed. The id would be the id for the feed.
We will store the last poll time of each feed and enqueue the next poll time accordingly.

## Note on interval:
We will queue the interval after the item finished downloading.

"""
import logging
from datetime import datetime

from krk.config import db
from pytz import UTC

from krk_v1.ctask import enq

l = logging.getLogger(__name__)


def run_poll():
    """
    Check the database and enqueue all the items for polling
    This function should be run every second.
    """

    to_poll = db["status"].find({"type": "poll"})

    for feed in to_poll:
        poll_time = feed["pollTime"]
        feed_id = feed["fid"]
        interval = feed["interval"]


def check_and_enq(feed_id, poll_time, interval):
    """
    Check the poll_time and enqueue the feed_id if now > poll_time

    :param str feed_id: ID of the feed to be check and possibly enqueue
    :param datetime poll_time: Poll time in UTC
    :param int interval: Interval (in seconds) to the next poll time.
    """

    if poll_time < datetime.now(tz=UTC):
        l.debug("Enqueuing %s, poll time %s", feed_id, poll_time.isoformat())
        enq.delay(feed_id, interval)
    else:
        l.debug("Feed %s poll at %s, the time is not yet ripe.", feed_id, poll_time.isoformat())
