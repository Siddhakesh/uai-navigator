"""
CampusNav Backend - Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
from app.db.json_adapter import JsonDBAdapter

mongo = JsonDBAdapter()


def create_app(config=None):
    app = Flask(__name__)

    # Default configuration
    app.config["MONGO_URI"] = "mongodb://localhost:27017/campusnav"
    app.config["SECRET_KEY"] = "campusnav-dev-secret-key-change-in-production"
    app.config["DEBUG"] = True

    if config:
        app.config.update(config)

    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    mongo.init_app(app)

    # Register blueprints
    from app.routes.checkpoints import bp as checkpoints_bp
    from app.routes.connections import bp as connections_bp
    from app.routes.destinations import bp as destinations_bp
    from app.routes.buildings import bp as buildings_bp
    from app.routes.routing import bp as routing_bp
    from app.routes.qr import bp as qr_bp
    from app.routes.admin import bp as admin_bp
    from app.routes.vision import bp as vision_bp

    app.register_blueprint(checkpoints_bp, url_prefix="/api")
    app.register_blueprint(connections_bp, url_prefix="/api")
    app.register_blueprint(destinations_bp, url_prefix="/api")
    app.register_blueprint(buildings_bp, url_prefix="/api")
    app.register_blueprint(routing_bp, url_prefix="/api")
    app.register_blueprint(qr_bp, url_prefix="/api")
    app.register_blueprint(admin_bp, url_prefix="/api")
    app.register_blueprint(vision_bp, url_prefix="/api")

    # Health check
    @app.route("/api/health")
    def health():
        return {"status": "ok", "service": "CampusNav API v1.0"}

    return app
