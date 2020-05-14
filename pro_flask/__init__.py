from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import import_string


db = SQLAlchemy()

blueprints = [
    'pro_flask.app01:app01',
]

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # load extensions
    db.init_app(app)

    # load blueprints
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    return app
