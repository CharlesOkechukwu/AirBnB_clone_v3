#!/usr/bin/python3
"""module to create view for user"""
from models.user import User
from models import storage
from flask import abort, jsonify, request
from . import app_views


@app_views.route("/users", methods=["GET", "POST"],
                 strict_slashes=False)
def get_users():
    """handle users by displaying all users
    or upload to users"""
    if request.method == "GET":
        states = storage.all(User)
        return jsonify([st.to_dict() for st in states.values()])
    else:
        body = request.get_json(force=True, silent=True)
        if body is None:
            abort(400, description="Not a JSON")
        if "name" not in body:
            abort(400, description="Missing Name")
        new = User(**body)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201


@app_views.route("/users/<user_id>",
                 methods=["GET", "PUT", "DELETE"],
                 strict_slashes=False)
def put_user(user_id):
    """get a user by id, update a user, delete a user
    using an id"""
    if request.method == "GET":
        obj = storage.get(User, str(user_id))
        if obj is None:
            abort(404, description="Not Found")
        return jsonify(obj.to_dict())
    elif request.method == "PUT":
        obj = storage.get(User, str(user_id))
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
        obj = storage.get(User, str(user_id))
        if obj is None:
            abort(404, description="Not Found")
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
