#!/usr/bin/python3
"""set up rotes for application"""
from models.city import City
from models.user import User
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from . import app_views
from models import storage
from flask import jsonify


@app_views.route("/status")
def status():
    """return status code of 200 OK"""
    return {"status": "OK"}


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def get_stat():
    """return the number of objects in each class"""
    clas = {"users": User, "states": State, "cities": City,
            "places": Place, "amenities": Amenity, "reviews": Review}
    stat = {}
    for key, value in clas.items():
        stat[key] = storage.count(value)
    return jsonify(stat)
