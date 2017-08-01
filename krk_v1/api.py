"""
API for krk

/feeds
GET: list all current feeds and information about each feed

/feed/<feed_id>
GET: information about a feed
PUT: update a feed record

/feed
POST: create new feed

/feed/<feed_id>/items
GET: list all items in the feed

/feed/<feed_id>/item/<item_id>
GET: information about an item

"""
import logging

from flask import Flask, jsonify

from krk_v1 import db

api = Flask(__name__)

l = logging.getLogger(__name__)


@api.route("/status")
def global_status():
    """
    Status for the whole system.

    :return:
    """
    return jsonify(list(db["status"].find()))


@api.route("/status/<what>")
def status_for(what):
    """
    Get status for an specific thing.

    :param what: the _id of the thing.
    :return: status of that thing.
    """
    status = db["status"].find_one({"_id": what})
    if not status:
        l.info("Can't find status for %s", what)
        return jsonify({"error": "can't find status of {}".format(what)})
    else:
        return jsonify(status)
