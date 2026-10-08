"""
Connections API Blueprint
Handles walking path connections between checkpoints.
"""
from flask import Blueprint, request, jsonify
from app import mongo

bp = Blueprint("connections", __name__)


def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc


@bp.route("/connections", methods=["GET"])
def get_connections():
    """Get all connections, optionally filtered by from/to checkpoint."""
    query = {}
    if request.args.get("from"):
        query["from_checkpoint"] = request.args.get("from")
    if request.args.get("to"):
        query["to_checkpoint"] = request.args.get("to")
    connections = list(mongo.db.connections.find(query))
    return jsonify([serialize(c) for c in connections])


@bp.route("/connections/<connection_id>", methods=["GET"])
def get_connection(connection_id):
    conn = mongo.db.connections.find_one({"connection_id": connection_id})
    if not conn:
        return jsonify({"error": "Connection not found"}), 404
    return jsonify(serialize(conn))


@bp.route("/connections", methods=["POST"])
def create_connection():
    """Create a new walking connection between two checkpoints."""
    data = request.get_json()
    required = ["connection_id", "from_checkpoint", "to_checkpoint"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # Check that checkpoints exist
    for cp_id in [data["from_checkpoint"], data["to_checkpoint"]]:
        if not mongo.db.checkpoints.find_one({"checkpoint_id": cp_id}):
            return jsonify({"error": f"Checkpoint '{cp_id}' not found"}), 404

    if mongo.db.connections.find_one({"connection_id": data["connection_id"]}):
        return jsonify({"error": "Connection ID already exists"}), 409

    # Auto-calculate walking time if not provided
    distance = data.get("distance", 50)
    walking_time = data.get("walking_time", round(distance / 1.4, 1))  # 1.4 m/s

    connection = {
        "connection_id": data["connection_id"],
        "from_checkpoint": data["from_checkpoint"],
        "to_checkpoint": data["to_checkpoint"],
        "distance": distance,
        "walking_time": walking_time,
        "accessible": data.get("accessible", True),
        "stairs": data.get("stairs", False),
        "ramp": data.get("ramp", False),
        "elevator": data.get("elevator", False),
        "is_active": data.get("is_active", True),
        "notes": data.get("notes", ""),
    }

    result = mongo.db.connections.insert_one(connection)
    connection["_id"] = str(result.inserted_id)
    return jsonify(connection), 201


@bp.route("/connections/<connection_id>", methods=["PUT"])
def update_connection(connection_id):
    data = request.get_json()
    data.pop("_id", None)
    data.pop("connection_id", None)

    result = mongo.db.connections.update_one(
        {"connection_id": connection_id},
        {"$set": data}
    )
    if result.matched_count == 0:
        return jsonify({"error": "Connection not found"}), 404

    updated = mongo.db.connections.find_one({"connection_id": connection_id})
    return jsonify(serialize(updated))


@bp.route("/connections/<connection_id>", methods=["DELETE"])
def delete_connection(connection_id):
    result = mongo.db.connections.delete_one({"connection_id": connection_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Connection not found"}), 404
    return jsonify({"message": f"Connection {connection_id} deleted"})
