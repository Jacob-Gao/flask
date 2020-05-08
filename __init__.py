from flask import Flask

def create_app():
    from . import gaochenpeng, yangzengpeng, zhangchunyi
    app = Flask(__name__)
    gaochenpeng.init_app(app)
    # yangzengpeng.init_app(app)
    # zhangchunyi.init_app(app)
    return app