from flask import Blueprint
from app.controllers.user_controller import (
    get_all_users,
    get_user,
    update_user,
    delete_user
)
from app.middlewares.auth_middleware import admin_required

user_bp = Blueprint("users", __name__)

user_bp.route("/", methods=["GET"])(admin_required(get_all_users))
user_bp.route("/<int:user_id>", methods=["GET"])(admin_required(get_user))
user_bp.route("/<int:user_id>", methods=["PUT"])(admin_required(update_user))
user_bp.route("/<int:user_id>", methods=["DELETE"])(admin_required(delete_user))