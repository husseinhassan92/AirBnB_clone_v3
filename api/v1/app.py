#!/usr/bin/python3

"""app for registering blueprint and starting flask"""
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(self):
    """close query after each session
    """
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """return JSON formatted 404 status code response"""
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
