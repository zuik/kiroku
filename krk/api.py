from flask import Flask, jsonify, request

from krk.config import db
from krk.feeds import add_feed, feed_info

api = Flask(__name__)


@api.route("/feeds")
def all_feeds():
    feeds = list(db["feeds"].find())

    return jsonify(feeds)


@api.route("/feed", methods=["POST", "GET"])
def feed_operations():
    if request.method == "POST":
        feed_name = request.form.get("feed_name")
        feed_url = request.form.get("feed_url")
        interval = request.form.get("interval")
        add_feed(feed_name=feed_name, feed_url=feed_url, interval=interval)
        return jsonify({"status": "ok"})
    elif request.method == "GET":
        feed_name = request.form.get("feed_name")
        return jsonify(feed_info(feed_name=feed_name))

if __name__ == '__main__':
    api.run(port=5001, debug=True)
