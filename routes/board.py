from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import (
    login_required,
    admin_required,
    csrf_required,
    new_csrf_token,
)

from models.board import Board


main = Blueprint('board', __name__)


@main.route("/admin")
@login_required
@admin_required
def index():
    token = new_csrf_token()
    return render_template('board/admin_index.html', token=token)


@main.route("/add", methods=["POST"])
@login_required
@admin_required
@csrf_required
def add():
    form = request.form
    Board.new(**form)
    return redirect(url_for('public.index'))

