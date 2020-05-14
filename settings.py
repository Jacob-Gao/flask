class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://jacob:jacob@127.0.0.1/flask_sql'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key_1'
    # SERVER_NAME = 'old.com:5000'



class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


