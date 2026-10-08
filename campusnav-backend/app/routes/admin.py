"""
Admin API Blueprint
Administrative operations: stats, bulk operations, graph management.
"""
from flask import Blueprint, request, jsonify
from app import mongo

bp = Blueprint("admin", __name__)


@bp.route("/admin/stats", methods=["GET"])
def get_stats():
    """Get campus navigation system statistics."""
    return jsonify({
        "checkpoints": {
            "total": mongo.db.checkpoints.count_documents({}),
            "active": mongo.db.checkpoints.count_documents({"is_active": True}),
        },
        "connections": {
            "total": mongo.db.connections.count_documents({}),
            "active": mongo.db.connections.count_documents({"is_active": True}),
            "with_stairs": mongo.db.connections.count_documents({"stairs": True}),
            "accessible": mongo.db.connections.count_documents({"accessible": True}),
        },
        "destinations": {
            "total": mongo.db.destinations.count_documents({}),
            "categories": mongo.db.destinations.distinct("category"),
        },
        "buildings": {
            "total": mongo.db.buildings.count_documents({}),
        },
    })


@bp.route("/admin/reset", methods=["POST"])
def reset_database():
    """Reset all navigation data (danger: destructive)."""
    data = request.get_json() or {}
    if data.get("confirm") != "RESET_ALL_DATA":
        return jsonify({"error": "Confirmation required: send confirm='RESET_ALL_DATA'"}), 400

    mongo.db.checkpoints.drop()
    mongo.db.connections.drop()
    mongo.db.destinations.drop()
    mongo.db.buildings.drop()

    return jsonify({"message": "All navigation data has been reset"})


@bp.route("/admin/seed", methods=["POST"])
def seed_database():
    """Seed database with UAI campus sample data."""
    from app.data.seed import get_seed_data
    
    seed = get_seed_data()
    
    # Clear existing
    mongo.db.checkpoints.drop()
    mongo.db.connections.drop()
    mongo.db.destinations.drop()
    mongo.db.buildings.drop()

    # Insert seed data
    if seed.get("buildings"):
        mongo.db.buildings.insert_many(seed["buildings"])
    if seed.get("checkpoints"):
        mongo.db.checkpoints.insert_many(seed["checkpoints"])
    if seed.get("connections"):
        mongo.db.connections.insert_many(seed["connections"])
    if seed.get("destinations"):
        mongo.db.destinations.insert_many(seed["destinations"])

    return jsonify({
        "message": "Database seeded with UAI campus data",
        "buildings": len(seed.get("buildings", [])),
        "checkpoints": len(seed.get("checkpoints", [])),
        "connections": len(seed.get("connections", [])),
        "destinations": len(seed.get("destinations", [])),
    })


@bp.route("/admin/export", methods=["GET"])
def export_data():
    """Export all campus navigation data as JSON."""
    checkpoints = list(mongo.db.checkpoints.find({}))
    connections = list(mongo.db.connections.find({}))
    destinations = list(mongo.db.destinations.find({}))
    buildings = list(mongo.db.buildings.find({}))

    for items in [checkpoints, connections, destinations, buildings]:
        for item in items:
            item["_id"] = str(item["_id"])

    return jsonify({
        "buildings": buildings,
        "checkpoints": checkpoints,
        "connections": connections,
        "destinations": destinations,
    })


@bp.route("/admin/import", methods=["POST"])
def import_data():
    """Import campus navigation data from JSON."""
    data = request.get_json()
    
    results = {}
    
    if data.get("buildings"):
        mongo.db.buildings.drop()
        mongo.db.buildings.insert_many(
            [{k: v for k, v in b.items() if k != "_id"} for b in data["buildings"]]
        )
        results["buildings"] = len(data["buildings"])

    if data.get("checkpoints"):
        mongo.db.checkpoints.drop()
        mongo.db.checkpoints.insert_many(
            [{k: v for k, v in c.items() if k != "_id"} for c in data["checkpoints"]]
        )
        results["checkpoints"] = len(data["checkpoints"])

    if data.get("connections"):
        mongo.db.connections.drop()
        mongo.db.connections.insert_many(
            [{k: v for k, v in c.items() if k != "_id"} for c in data["connections"]]
        )
        results["connections"] = len(data["connections"])

    if data.get("destinations"):
        mongo.db.destinations.drop()
        mongo.db.destinations.insert_many(
            [{k: v for k, v in d.items() if k != "_id"} for d in data["destinations"]]
        )
        results["destinations"] = len(data["destinations"])

    return jsonify({"message": "Import successful", "imported": results})
