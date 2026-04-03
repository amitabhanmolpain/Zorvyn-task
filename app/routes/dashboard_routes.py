from flask import Blueprint
from app.controllers.dashboard_controller import get_summary
from app.middlewares.auth_middleware import analyst_required

dashboard_bp = Blueprint("dashboard", __name__)

dashboard_bp.route("/summary", methods=["GET"])(analyst_required(get_summary))