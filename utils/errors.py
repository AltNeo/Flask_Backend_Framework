from flask import jsonify
from functools import wraps

class APIError(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['success'] = False
        return rv

def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def validate_request(*required_fields):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.form:
                raise APIError("No form data provided", 400)
            for field in required_fields:
                if field not in request.form:
                    raise APIError(f"Missing required field: {field}", 400)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
