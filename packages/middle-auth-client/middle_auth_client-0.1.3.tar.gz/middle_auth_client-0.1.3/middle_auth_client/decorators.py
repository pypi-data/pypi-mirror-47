from functools import wraps
import flask
import json
import os
import redis

r = redis.Redis(
        host=os.environ.get('REDISHOST', 'localhost'),
        port=int(os.environ.get('REDISPORT', 6379)))

AUTH_URI = os.environ.get('AUTH_URI', 'localhost:5000/auth')


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = flask.request.headers.get('authorization')
        if not token:
            resp = flask.Response("Unauthorized", 401)
            resp.headers['WWW-Authenticate'] = 'Bearer realm="' + AUTH_URI + '"'
            return resp
        elif not token.startswith('Bearer '):
            resp = flask.Response("Invalid Request", 400)
            resp.headers['WWW-Authenticate'] = 'Bearer realm="' + AUTH_URI + '", error="invalid_request", error_description="Header must begin with \'Bearer\'"'
            return resp
        else:
            token = token.split(' ')[1] # remove schema
            cached_user_data = r.get("token_" + token)

            if cached_user_data:
                flask.g.auth_user = json.loads(cached_user_data.decode('utf-8'))
                flask.g.auth_token = token
                return f(*args, **kwargs)
            else:
                resp = flask.Response("Invalid/Expired Token", 401)
                resp.headers['WWW-Authenticate'] = 'Bearer realm="' + AUTH_URI + '", error="invalid_token", error_description="Invalid/Expired Token"'
                return resp
    return decorated_function

def requires_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if role in flask.g.auth_user['roles']:
                return f(*args, **kwargs)
            else:
                resp = flask.Response("Missing role: {0}".format(role), 403)
                return resp
           
        return decorated_function
    return decorator
