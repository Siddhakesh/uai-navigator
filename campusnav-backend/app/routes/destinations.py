"""
Destinations API Blueprint
Handles destinations that users navigate to (offices, labs, departments, etc).
"""
from flask import Blueprint, request, jsonify
from app import mongo
import re

bp = Blueprint("destinations", __name__)


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


@bp.route("/destinations", methods=["GET"])
def get_destinations():
    """Get destinations with optional search query."""
    query_str = request.args.get("q", "").strip()
    category = request.args.get("category", "")
    
    query = {}
    if query_str:
        pattern = re.compile(query_str, re.IGNORECASE)
        query["$or"] = [
            {"name": {"$regex": pattern}},
            {"aliases": {"$elemMatch": {"$regex": pattern}}},
            {"description": {"$regex": pattern}},
        ]
    if category:
        query["category"] = category

    destinations = list(mongo.db.destinations.find(query).limit(50))
    return jsonify([serialize(d) for d in destinations])


@bp.route("/destinations/<destination_id>", methods=["GET"])
def get_destination(destination_id):
    dest = mongo.db.destinations.find_one({"destination_id": destination_id})
    if not dest:
        return jsonify({"error": "Destination not found"}), 404
    return jsonify(serialize(dest))


@bp.route("/destinations/categories", methods=["GET"])
def get_categories():
    """Get distinct destination categories."""
    categories = mongo.db.destinations.distinct("category")
    return jsonify(categories)


@bp.route("/destinations", methods=["POST"])
def create_destination():
    data = request.get_json()
    required = ["destination_id", "name", "checkpoint_id"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    if mongo.db.destinations.find_one({"destination_id": data["destination_id"]}):
        return jsonify({"error": "Destination ID already exists"}), 409

    destination = {
        "destination_id": data["destination_id"],
        "name": data["name"],
        "aliases": data.get("aliases", []),
        "checkpoint_id": data["checkpoint_id"],
        "building_id": data.get("building_id"),
        "floor": data.get("floor", 0),
        "category": data.get("category", "general"),
        "description": data.get("description", ""),
        "is_active": data.get("is_active", True),
        "icon": data.get("icon", "📍"),
    }

    result = mongo.db.destinations.insert_one(destination)
    destination["_id"] = str(result.inserted_id)
    return jsonify(destination), 201


@bp.route("/destinations/<destination_id>", methods=["PUT"])
def update_destination(destination_id):
    data = request.get_json()
    data.pop("_id", None)
    data.pop("destination_id", None)

    result = mongo.db.destinations.update_one(
        {"destination_id": destination_id},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Destination not found"}), 404

    updated = mongo.db.destinations.find_one({"destination_id": destination_id})
    return jsonify(serialize(updated))


@bp.route("/destinations/<destination_id>", methods=["DELETE"])
def delete_destination(destination_id):
    result = mongo.db.destinations.delete_one({"destination_id": destination_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Destination not found"}), 404
    return jsonify({"message": f"Destination {destination_id} deleted"})
