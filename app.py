import time
import config

from flask import Flask, g

from routes import current_user

from routes.public import main as public_routes
from routes.user import main as user_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.mail import main as mail_routes
from routes.error import main as error_routes


def count(input):
    return len(input)


class Elapse:
    minute = 60
    hour = 60 * 60
    day = 60 * 60 * 24


def moment(passed):
    """
    xxx秒前
    :param passed: time.time()
    :return: str xxx[秒分时天]
    """
    now = time.time()
    elapse = now - passed
    if elapse < Elapse.minute:
        word = '{}秒前'.format(int(elapse))
    elif Elapse.minute < elapse < Elapse.hour:
        word = '{}分钟前'.format(int(elapse / Elapse.minute))
    elif Elapse.hour < elapse < Elapse.day:
        word = '{}小时前'.format(int(elapse / Elapse.hour))
    else:
        word = '{}天前'.format(int(elapse / Elapse.day))

    return word


def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    # 这个字符串随便你设置什么内容都可以
    app.secret_key = config.secret_key

    @app.before_request
    def app_before_req():
        # 每次请求获取当前用户，设置全局变量
        g.user = current_user()

    app.register_blueprint(public_routes)
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(error_routes)

    app.add_template_filter(count)
    app.add_template_filter(moment)

    return app


# 运行代码
if __name__ == '__main__':
    # app.add_template_filter(count)
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # 自动 reload jinja
    app = configured_app()
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
    )
    app.run(**config)
