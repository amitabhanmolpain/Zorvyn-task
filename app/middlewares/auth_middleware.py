from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def roles_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)

            if not user:
                return jsonify({"error": "User not found"}), 404

            if not user.is_active:
                return jsonify({"error": "Account is inactive"}), 403

            if user.role not in roles:
                return jsonify({
                    "error": f"Access denied. Required roles: {list(roles)}"
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper



def admin_required(fn):
    return roles_required("admin")(fn)

def analyst_required(fn):
    return roles_required("analyst", "admin")(fn)

def viewer_required(fn):
    return roles_required("viewer", "analyst", "admin")(fn)