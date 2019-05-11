import uuid

import os
from flask import (
    render_template,
    flash,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
)

from routes import (
    current_user,
    login_required,
    csrf_required,
    new_csrf_token,
)

from models.topic import Topic
from models.user import User

main = Blueprint('user', __name__)


@main.route("/register/view")
def register_view():
    user = current_user()

    if user.username != '游客':
        return redirect('/')

    token = new_csrf_token()
    return render_template('user/register.html', token=token)


@main.route("/register", methods=['POST'])
@csrf_required
def register():
    form = request.form
    u, result = User.register(form.to_dict())
    flash(result)
    return redirect(url_for('.register_view'))


@main.route("/login/view")
def login_view():
    user = current_user()

    if user.username != '游客':
        return redirect(url_for('public.index'))

    token = new_csrf_token()
    return render_template('user/login.html', token=token)


@main.route("/login", methods=['POST'])
@csrf_required
def login():
    form = request.form
    u, result = User.validate_login(form)

    if u is None:
        flash(result)
        return redirect(url_for('.login_view'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('public.index'))


@main.route("/logout")
@login_required
@csrf_required
def logout():
    session.pop('user_id')
    return redirect(url_for('public.index'))


@main.route('/<username>')
def detail(username):
    u = User.one(username=username)
    t = Topic.recent_created_topics(u)
    t2 = Topic.recent_join_topics(u)
    token = new_csrf_token()

    if u is None:
        abort(404)
    else:
        return render_template(
            'user/detail.html',
            user=u, ms=t, ms2=t2, token=token
        )


@main.route("/setting")
@login_required
def setting():
    """
    用户设置页
    """
    token = new_csrf_token()
    return render_template('user/setting.html', token=token)


@main.route("/info/update", methods=['POST'])
@login_required
@csrf_required
def info_update():
    form = request.form.to_dict()
    u = User.one(username=form['username'])
    if not u:
        flash('用户名已被占用')
    else:
        flash('用户信息修改成功')
        User.update(u.id, **form)

    return redirect(url_for('.setting'))


@main.route("/password/update", methods=['POST'])
@login_required
@csrf_required
def password_update():
    form = request.form
    u = current_user()
    u, result = User.update_password(u.id, form)

    flash(result)
    return redirect(url_for('.setting'))


@main.route('/image/add', methods=['POST'])
@login_required
@csrf_required
def image_add():
    file = request.files['avatar']

    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    id = u.id
    images = dict(
        image='/images/{}'.format(filename),
    )
    m = User.update(id, **images)
    flash('头像修改成功')

    return redirect(url_for('.setting'))
