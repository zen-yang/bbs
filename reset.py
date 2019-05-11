import config
from models import reset_database
from models.user import User
from models.user_role import UserRole
from models.board import Board
from models.mail import Mail
from models.reply import Reply
from models.topic import Topic
from utils import log


def register_admin():
    form = dict(
        username=config.admin_username,
        password=config.admin_password,
        role=UserRole.admin,
    )

    u, result = User.register(form)
    log(u, result)


def main():
    reset_database()
    register_admin()


if __name__ == '__main__':
    main()
