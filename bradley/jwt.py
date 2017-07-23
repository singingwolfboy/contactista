import datetime
import jwt
from flask import current_app
from bradley.models.auth import User


JWT_HEADER_NAME = 'Authorization'
JWT_SCHEMA = 'Bearer'
JWT_ALGORITHM = 'HS256'
JWT_LIFETIME = datetime.timedelta(days=7)


def jwt_token_for_user(user):
    now = datetime.datetime.utcnow()
    payload = {
        "iat": now,
        "exp": now + JWT_LIFETIME,
        "identity": user.id,
    }
    return jwt.encode(
        payload,
        key=current_app.config['SECRET_KEY'],
        algorithm=JWT_ALGORITHM,
    )


def jwt_token_from_request(request):
    header = request.headers.get(JWT_HEADER_NAME, None)
    if header and header.startswith(JWT_SCHEMA + " "):
        return header[len(JWT_SCHEMA) + 1:]
    return None


def user_from_jwt_request(request):
    token = jwt_token_from_request(request)
    if not token:
        return None
    payload = jwt.decode(
        token,
        key=current_app.config['SECRET_KEY'],
        algorithms=[JWT_ALGORITHM],
    )
    return User.query.filter(User.id == payload['identity']).scalar()
