import uuid
from functools import wraps

from flask import (
    session,
    request,
    abort,
    redirect,
    url_for,
)

from models.user import User


def current_user():
    """
    从 session 中找到 user_id 字段
    找不到就返回 guest
    """
    if 'user_id' in session:
        uid = int(session['user_id'])
        e = User.exist(id=uid)
        if e:
            return User.one(id=uid)
        else:
            return User.guest()
    else:
        return User.guest()


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = current_user()
        if not u.is_guest():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('user.login_view'))

    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        u = current_user()
        if u.is_admin():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('public.index'))

    return wrapper


csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'token' in session and 'token' in request.args:
            token_session = session['token']
            token_get = request.args['token']

            if token_get == token_session:
                return f(*args, **kwargs)
            else:
                abort(401)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    token_session = str(uuid.uuid4())
    session['token'] = token_session

    return token_session
