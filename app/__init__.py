from flask import Flask
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

    
    return app
