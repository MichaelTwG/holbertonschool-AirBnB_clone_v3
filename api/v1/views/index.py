#!/usr/bin/python
""" Index file """
from api.v1.views.__init__ import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    return jsonify({"status": "OK"})
