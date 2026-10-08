"""
Buildings API Blueprint
"""
from flask import Blueprint, request, jsonify
from app import mongo

bp = Blueprint("buildings", __name__)


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


@bp.route("/buildings", methods=["GET"])
def get_buildings():
    buildings = list(mongo.db.buildings.find({}))
    return jsonify([serialize(b) for b in buildings])


@bp.route("/buildings/<building_id>", methods=["GET"])
def get_building(building_id):
    building = mongo.db.buildings.find_one({"building_id": building_id})
    if not building:
        return jsonify({"error": "Building not found"}), 404
    return jsonify(serialize(building))


@bp.route("/buildings", methods=["POST"])
def create_building():
    data = request.get_json()
    if not data.get("building_id") or not data.get("name"):
        return jsonify({"error": "building_id and name are required"}), 400

    if mongo.db.buildings.find_one({"building_id": data["building_id"]}):
        return jsonify({"error": "Building ID already exists"}), 409

    building = {
        "building_id": data["building_id"],
        "name": data["name"],
        "description": data.get("description", ""),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "polygon": data.get("polygon", []),  # List of [lat, lng] or [x, y] coords
        "floors": data.get("floors", 1),
        "color": data.get("color", "#3B82F6"),
    }

    result = mongo.db.buildings.insert_one(building)
    building["_id"] = str(result.inserted_id)
    return jsonify(building), 201


@bp.route("/buildings/<building_id>", methods=["PUT"])
def update_building(building_id):
    data = request.get_json()
    data.pop("_id", None)
    data.pop("building_id", None)

    result = mongo.db.buildings.update_one(
        {"building_id": building_id},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Building not found"}), 404

    updated = mongo.db.buildings.find_one({"building_id": building_id})
    return jsonify(serialize(updated))


@bp.route("/buildings/<building_id>", methods=["DELETE"])
def delete_building(building_id):
    result = mongo.db.buildings.delete_one({"building_id": building_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Building not found"}), 404
    return jsonify({"message": f"Building {building_id} deleted"})
