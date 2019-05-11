from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import (
    current_user,
    login_required,
    csrf_required,
    new_csrf_token,
)

from models.mail import Mail

main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    form['receiver_id'] = int(form['receiver_id'])
    u = current_user()
    form['sender_id'] = u.id

    m = Mail.new(**form)
    return redirect(url_for('.index'))


@main.route('/')
@login_required
def index():
    u = current_user()

    sent_mail = Mail.all(sender_id=u.id)
    received_mail = Mail.all(receiver_id=u.id)

    token = new_csrf_token()
    t = render_template(
        'mail/index.html',
        send=sent_mail,
        received=received_mail,
        token=token,
    )
    return t


@main.route('/view/<int:id>')
@login_required
def view(id):
    mail = Mail.one(id=id)
    u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    if u.id in [mail.receiver_id, mail.sender_id]:
        return render_template('mail/detail.html', mail=mail)
    else:
        return redirect(url_for('.index'))
