from flask import (
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.mail import Mail
from models.reply import Reply
from models.user import User
from routes import (
    current_user,
    login_required,
    csrf_required,
)

main = Blueprint('reply', __name__)


def users_from_content(content):
    # 内容 @123 内容
    # 如果用户名含有空格 就不行了 @name 123
    parts = content.split(' ')
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            users.append(u)

    return users


def send_mails(sender, receivers, content):
    for r in receivers:
        form = dict(
            title='你被 {} AT 了'.format(sender.username),
            content=content,
            sender_id=sender.id,
            receiver_id=r.id
        )
        Mail.new(**form)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form
    u = current_user()

    content = form['content']
    users = users_from_content(content)
    send_mails(u, users, content)

    form = dict(
        content=content,
        topic_id=form['topic_id'],
        user_id=u.id
    )

    m = Reply.new(**form)
    return redirect(url_for('topic.detail', id=m.topic_id))

