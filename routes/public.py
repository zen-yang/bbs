from flask import (
    request,
    render_template,
    Blueprint,
)

from routes import (
    current_user,
    new_csrf_token,
)

from models.topic import Topic
from models.board import Board

main = Blueprint('public', __name__)


@main.route("/")
def index():
    u = current_user()
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    ms.sort(key=lambda ms: ms.created_time, reverse=True)
    token = new_csrf_token()
    bs = Board.all()
    return render_template("index.html", user=u, ms=ms, token=token, bs=bs, bid=board_id)
