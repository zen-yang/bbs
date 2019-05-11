from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import (
    current_user,
    login_required,
    new_csrf_token,
    csrf_required,
    admin_required,
)

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route('/<int:id>')
def detail(id):
    t = Topic.get(id)
    if t is not None:
        token = new_csrf_token()
        return render_template("topic/detail.html", topic=t, token=token)
    else:
        return abort(404)


@main.route("/delete")
@login_required
@admin_required
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    Topic.delete(id)

    return redirect(url_for('public.index'))


@main.route("/new")
@login_required
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, token=token, bid=board_id)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form
    u = current_user()
    add_form = dict(
        title=form['title'],
        content=form['content'],
        user_id=u.id,
        board_id=form['board_id'],
    )
    Topic.new(**add_form)
    return redirect(url_for('public.index'))


@main.route('/admin')
@login_required
@admin_required
def admin():
    ts = Topic.all()
    token = new_csrf_token()
    return render_template("topic/admin.html", topics=ts, token=token)
