from flask import Flask, jsonify

from krk.config import db

api = Flask(__name__)


@api.route("/feeds")
def all_feeds():
    feeds = list(db["feeds"].find())

    return jsonify(feeds)


if __name__ == '__main__':
    api.run(port=5001, debug=True)
