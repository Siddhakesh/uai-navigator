"""
Routing API Blueprint
Exposes the A* routing engine via REST API.
"""
from flask import Blueprint, request, jsonify
from app import mongo
from app.routing.engine import find_route

bp = Blueprint("routing", __name__)


@bp.route("/route", methods=["GET"])
def calculate_route():
    """
    Calculate the best walking route between two checkpoints.
    
    Query parameters:
      from  - Starting checkpoint_id (e.g. CP001)
      to    - Destination checkpoint_id (e.g. CP009)
      mode  - Route mode: fastest | shortest | accessible (default: fastest)
    """
    from_id = request.args.get("from")
    to_id = request.args.get("to")
    mode = request.args.get("mode", "fastest")

    if not from_id or not to_id:
        return jsonify({"error": "Both 'from' and 'to' parameters are required"}), 400

    if mode not in ("fastest", "shortest", "accessible"):
        return jsonify({"error": "Invalid mode. Use: fastest, shortest, accessible"}), 400

    if from_id == to_id:
        return jsonify({"error": "Start and destination cannot be the same"}), 400

    # Load graph data from DB
    checkpoints = list(mongo.db.checkpoints.find({"is_active": True}))
    connections = list(mongo.db.connections.find({"is_active": True}))

    # Strip ObjectId for routing engine
    for cp in checkpoints:
        cp.pop("_id", None)
    for conn in connections:
        conn.pop("_id", None)

    result = find_route(checkpoints, connections, from_id, to_id, mode)

    if "error" in result:
        return jsonify(result), 404

    return jsonify(result)


@bp.route("/route/by-destination", methods=["GET"])
def route_by_destination():
    """
    Calculate route where destination is a destination_id (not checkpoint_id).
    Resolves destination to checkpoint_id, then calls routing engine.
    """
    from_id = request.args.get("from")
    dest_id = request.args.get("destination")
    mode = request.args.get("mode", "fastest")

    if not from_id or not dest_id:
        return jsonify({"error": "'from' and 'destination' parameters are required"}), 400

    # Resolve destination to checkpoint
    dest = mongo.db.destinations.find_one({"destination_id": dest_id})
    if not dest:
        return jsonify({"error": f"Destination '{dest_id}' not found"}), 404

    to_id = dest["checkpoint_id"]

    # Load graph
    checkpoints = list(mongo.db.checkpoints.find({"is_active": True}))
    connections = list(mongo.db.connections.find({"is_active": True}))

    for cp in checkpoints:
        cp.pop("_id", None)
    for conn in connections:
        conn.pop("_id", None)

    result = find_route(checkpoints, connections, from_id, to_id, mode)

    if "error" in result:
        return jsonify(result), 404

    result["destination"] = {
        "destination_id": dest["destination_id"],
        "name": dest["name"],
        "description": dest.get("description", ""),
        "category": dest.get("category", ""),
    }

    return jsonify(result)


@bp.route("/graph", methods=["GET"])
def get_graph():
    """Return the full campus graph for admin visualization."""
    checkpoints = list(mongo.db.checkpoints.find({}))
    connections = list(mongo.db.connections.find({}))

    for cp in checkpoints:
        cp["_id"] = str(cp["_id"])
    for conn in connections:
        conn["_id"] = str(conn["_id"])

    return jsonify({
        "checkpoints": checkpoints,
        "connections": connections,
        "stats": {
            "total_checkpoints": len(checkpoints),
            "total_connections": len(connections),
            "active_checkpoints": sum(1 for c in checkpoints if c.get("is_active", True)),
            "active_connections": sum(1 for c in connections if c.get("is_active", True)),
        }
    })
