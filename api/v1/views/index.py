#!/usr/bin/python3
"""set up rotes for application"""
from . import app_views


@app_views.route("/status")
def status():
    """return status code of 200 OK"""
    return {"status": "OK"}
