#!/usr/bin/python3
"""module to create view for Amenity"""
from models.amenity import Amenity
from models import storage
from flask import abort, jsonify, request
from . import app_views


@app_views.route("/amenities", methods=["GET", "POST"],
                 strict_slashes=False)
def get_amenity():
    """handle amenities by displaying all amenities
    or upload to amenity"""
    if request.method == "GET":
        states = storage.all(Amenity)
        return jsonify([st.to_dict() for st in states.values()])
    else:
        body = request.get_json(force=True, silent=True)
        if body is None:
            abort(400, description="Not a JSON")
        if "name" not in body:
            abort(400, description="Missing Name")
        new = Amenity(**body)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """get a state by id, update a state, delete a state
    using an id"""
    if request.method == "GET":
        obj = storage.get(Amenity, str(amenity_id))
        if obj is None:
            abort(404, description="Not Found")
        return jsonify(obj.to_dict())
    elif request.method == "PUT":
        obj = storage.get(Amenity, str(amenity_id))
        if obj is None:
            abort(404, description="Not Found")
        body = request.get_json(force=True, silent=True)
        if body is None:
            abort(400, description="Not a JSON")
        for k, v in body.items():
            if k not in ["created_at", "updated_at", "id"]:
                setattr(obj, k, v)
        obj.save()
        return jsonify(obj.to_dict()), 200
    else:
        obj = storage.get(Amenity, str(amenity_id))
        if obj is None:
            abort(404, description="Not Found")
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
