import hashlib
import config
from sqlalchemy import (
    Column,
    String,
    Enum,
)

from models import (
    SQLMixin,
    SQLBase,
)
from models.user_role import UserRole


class User(SQLMixin, SQLBase):
    __tablename__ = 'User'
    """
    User 是一个保存用户数据的 model
    """
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.normal)
    image = Column(String(100), nullable=False, default='/images/moren.jpg')
    signature = Column(String(200), nullable=False, default='')

    def add_default_value(self):
        super().add_default_value()
        self.password = self.salted_password(self.password)

    @staticmethod
    def salted_password(password, salt=config.salt):
        salted = hashlib.sha256((str(password) + salt).encode('ascii')).hexdigest()
        return salted

    @classmethod
    def register(cls, form):
        if not len(form['username']) > 3:
            return None, '用户名长度必须大于3'
        if not len(form['password']) > 5:
            return None, '密码长度必须大于5'
        if cls.exist(username=form['username']):
            return None, '用户名已被注册'

        u = User.new(**form)

        return u, '用户注册成功'

    @classmethod
    def validate_login(cls, form):
        username = form['username']
        if User.exist(username=username):
            u = User.one(username=username)
            password = u.salted_password(form['password'])

            query = dict(
                username=username,
                password=password,
            )

            if User.exist(**query):
                u = User.one(**query)
                return u, '登陆成功'
            else:
                return None, '用户名或密码错误'
        else:
            return None, '用户不存在'

    @classmethod
    def update_password(cls, id, form):
        if cls.exist(id=id):
            u = cls.one(id=id)
            op = u.salted_password(form['old_password'])

            if op == u.password:
                np = form['new_password']

                if len(np) > 5:
                    np = u.salted_password(np)
                    u = cls.update(id, password=np)
                    return u, '密码更新成功'
                else:
                    return None, '新密码不满足要求'
            else:
                return None, '当前密码错误'
        else:
            return None, '用户不存在'

    @classmethod
    def guest(cls):
        u = cls()
        u.username = '游客'
        u.role = UserRole.guest
        return u

    def is_guest(self):
        return self.role == UserRole.guest

    def is_admin(self):
        return self.role == UserRole.admin
