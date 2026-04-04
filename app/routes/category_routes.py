from flask import Blueprint
from app.controllers.category_controller import (
    get_all_categories,
    create_category,
    delete_category
)
from app.middlewares.auth_middleware import viewer_required, admin_required


category_bp = Blueprint("categories", __name__)

category_bp.route("/", methods=["GET"])(viewer_required(get_all_categories))
category_bp.route("/", methods=["POST"])(admin_required(create_category))
category_bp.route("/<int:category_id>", methods=["DELETE"])(admin_required(delete_category))