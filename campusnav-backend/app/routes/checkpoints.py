"""
Checkpoints API Blueprint
Handles CRUD operations for campus navigation checkpoints.
"""
from flask import Blueprint, request, jsonify
from bson import ObjectId
from app import mongo

bp = Blueprint("checkpoints", __name__)


def serialize_checkpoint(cp):
    cp["_id"] = str(cp["_id"])
    return cp


@bp.route("/checkpoints", methods=["GET"])
def get_checkpoints():
    """Get all active checkpoints."""
    only_active = request.args.get("active", "true").lower() == "true"
    query = {"is_active": True} if only_active else {}
    checkpoints = list(mongo.db.checkpoints.find(query))
    return jsonify([serialize_checkpoint(c) for c in checkpoints])


@bp.route("/checkpoints/<checkpoint_id>", methods=["GET"])
def get_checkpoint(checkpoint_id):
    """Get a single checkpoint by its checkpoint_id (e.g. CP001)."""
    cp = mongo.db.checkpoints.find_one({"checkpoint_id": checkpoint_id})
    if not cp:
        return jsonify({"error": "Checkpoint not found"}), 404
    return jsonify(serialize_checkpoint(cp))


@bp.route("/checkpoints", methods=["POST"])
def create_checkpoint():
    """Create a new checkpoint."""
    data = request.get_json()
    required = ["checkpoint_id", "name"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Check duplicate
    if mongo.db.checkpoints.find_one({"checkpoint_id": data["checkpoint_id"]}):
        return jsonify({"error": "Checkpoint ID already exists"}), 409

    checkpoint = {
        "checkpoint_id": data["checkpoint_id"],
        "name": data["name"],
        "description": data.get("description", ""),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
        "map_x": data.get("map_x"),
        "map_y": data.get("map_y"),
        "building_id": data.get("building_id"),
        "floor": data.get("floor", 0),
        "type": data.get("type", "checkpoint"),
        "is_active": data.get("is_active", True),
        "icon": data.get("icon", "default"),
    }

    result = mongo.db.checkpoints.insert_one(checkpoint)
    checkpoint["_id"] = str(result.inserted_id)
    return jsonify(checkpoint), 201


@bp.route("/checkpoints/<checkpoint_id>", methods=["PUT"])
def update_checkpoint(checkpoint_id):
    """Update an existing checkpoint."""
    data = request.get_json()
    data.pop("_id", None)
    data.pop("checkpoint_id", None)

    result = mongo.db.checkpoints.update_one(
        {"checkpoint_id": checkpoint_id},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Checkpoint not found"}), 404

    updated = mongo.db.checkpoints.find_one({"checkpoint_id": checkpoint_id})
    return jsonify(serialize_checkpoint(updated))


@bp.route("/checkpoints/<checkpoint_id>", methods=["DELETE"])
def delete_checkpoint(checkpoint_id):
    """Delete a checkpoint."""
    result = mongo.db.checkpoints.delete_one({"checkpoint_id": checkpoint_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Checkpoint not found"}), 404
    return jsonify({"message": f"Checkpoint {checkpoint_id} deleted"})
