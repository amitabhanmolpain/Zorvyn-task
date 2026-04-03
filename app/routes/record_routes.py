from flask import Blueprint
from app.controllers.record_controller import (
    get_all_records,
    get_record,
    create_record,
    update_record,
    delete_record
)
from app.middlewares.auth_middleware import (
    admin_required,
    viewer_required
)

record_bp = Blueprint("records", __name__)

# All logged in users can view
record_bp.route("/", methods=["GET"])(viewer_required(get_all_records))
record_bp.route("/<int:record_id>", methods=["GET"])(viewer_required(get_record))

# Only admin can create, update, delete
record_bp.route("/", methods=["POST"])(admin_required(create_record))
record_bp.route("/<int:record_id>", methods=["PUT"])(admin_required(update_record))
record_bp.route("/<int:record_id>", methods=["DELETE"])(admin_required(delete_record))