from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from models import User

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            if not user or not user.is_admin:
                return jsonify({"message": "Permission denied: Admin access required"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
