from flask import Blueprint
from app.controllers.auth_controller import register, login, me
from app.extensions import limiter

auth_bp = Blueprint("auth", __name__)

auth_bp.route("/register", methods=["POST"])(limiter.limit("5 per minute")(register))
auth_bp.route("/login", methods=["POST"])(limiter.limit("10 per minute")(login))
auth_bp.route("/me", methods=["GET"])(me)