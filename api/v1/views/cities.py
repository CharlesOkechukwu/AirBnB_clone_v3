#!/usr/bin/python3
"""module to create view for cities"""
from models.city import City
from models.state import State
from models import storage
from flask import abort, jsonify, request
from . import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET", "POST"],
                 strict_slashes=False)
def get_cities(state_id):
    """handle states states by displaying all states
    or upload to states"""
    states = storage.get(State, str(state_id))
    if states is None:
        abort(404, description="Not Found")
    if request.method == "GET":
        return jsonify([ct.to_dict() for ct in states.cities])
    else:
        body = request.get_json(force=True, silent=True)
        if body is None:
            abort(400, description="Not a JSON")
        if "name" not in body:
            abort(400, description="Missing Name")
        body.update({"state_id": str(state_id)})
        new = City(**body)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201


@app_views.route("/cities/<city_id>",
                 methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def put_city(city_id):
    """get a city by id, update a city, delete a city
    using an id"""
    if request.method == "GET":
        obj = storage.get(City, str(city_id))
        if obj is None:
            abort(404, description="Not Found")
        return jsonify(obj.to_dict())
    elif request.method == "PUT":
        obj = storage.get(City, str(city_id))
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
        obj = storage.get(City, str(city_id))
        if obj is None:
            abort(404, description="Not Found")
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
