from flask import Flask, jsonify
import importlib

from .config import Config
from .extensions import db, migrate, jwt, bcrypt, ma

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    from . import models  # noqa: F401

    route_modules = (
        (".routes.auth_routes", "auth_bp", "/api/auth"),
        (".routes.user_routes", "user_bp", "/api/users"),
        (".routes.record_routes", "record_bp", "/api/records"),
        (".routes.dashboard_routes", "dashboard_bp", "/api/dashboard"),
    )

    for module_path, blueprint_name, url_prefix in route_modules:
        try:
            module = importlib.import_module(module_path, package=__name__)
        except ModuleNotFoundError:
            continue
        app.register_blueprint(getattr(module, blueprint_name), url_prefix=url_prefix)

    from .routes.category_routes import category_bp
    app.register_blueprint(category_bp, url_prefix="/api/categories")

    @app.errorhandler(400)
    def handle_bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(401)
    def handle_unauthorized(error):
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(403)
    def handle_access_denied(error):
        return jsonify({"error": "Access denied"}), 403

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def handle_internal_server_error(error):
        return jsonify({"error": "Internal server error"}), 500

    
    return app
