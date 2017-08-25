import datetime
import jwt
from flask import current_app
from bradley.models.auth import User


JWT_HEADER_NAME = 'Authorization'
JWT_SCHEMA = 'Bearer'
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = datetime.timedelta(seconds=300)
JWT_ALLOW_REFRESH = True
JWT_REFRESH_EXPIRATION_DELTA = datetime.timedelta(days=7)


def jwt_payload(user):
    now = datetime.datetime.utcnow()
    payload = {
        "iat": int(now.timestamp()),
        "exp": int((now + JWT_EXPIRATION_DELTA).timestamp()),
        "identity": user.id,
    }
    if JWT_ALLOW_REFRESH:
        payload["orig_iat"] = payload["iat"]
    return payload


def jwt_token_for_user(user):
    return jwt.encode(
        jwt_payload(user),
        key=current_app.config['SECRET_KEY'],
        algorithm=JWT_ALGORITHM,
    )


def refresh_jwt_token(token):
    payload = jwt.decode(
        token,
        key=current_app.config['SECRET_KEY'],
        algorithms=[JWT_ALGORITHM],
    )
    user = User.query.get(payload['identity'])
    if not user.active:
        raise ValueError("User is inactive")
    orig_iat = payload.get('orig_iat')
    if not orig_iat:
        raise ValueError("`orig_iat` field is required")
    refresh_limit = orig_iat + int(JWT_REFRESH_EXPIRATION_DELTA.total_seconds())
    now_ts = datetime.datetime.utcnow().timestamp()
    if now_ts > refresh_limit:
        raise ValueError("Refresh has expired")
    new_payload = jwt_payload(user)
    new_payload["orig_iat"] = orig_iat
    token = jwt.encode(
        new_payload,
        key=current_app.config['SECRET_KEY'],
        algorithm=JWT_ALGORITHM,
    )
    return token, user


def jwt_token_from_request(request):
    header = request.headers.get(JWT_HEADER_NAME, None)
    if header and header.startswith(JWT_SCHEMA + " "):
        return header[len(JWT_SCHEMA) + 1:]
    return None


def user_from_jwt_request(request):
    token = jwt_token_from_request(request)
    if not token:
        return None
    try:
        payload = jwt.decode(
            token,
            key=current_app.config['SECRET_KEY'],
            algorithms=[JWT_ALGORITHM],
        )
    except jwt.exceptions.DecodeError:
        return None
    return User.query.get(payload['identity'])
