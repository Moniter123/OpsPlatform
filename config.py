import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1qaz2wsx'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    BABEL_DEFAULT_LOCALE = 'zh'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@127.0.0.1/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
#    SQLALCHEMY_ECHO = True


    #RECAPTCHA_PUBLIC_KEY = '1qaz2wsx3edc'
    #RECAPTCHA_PRIVATE_KEY = '1dfdewdf3dsfdsa'


class TestingConfig(Config):
    TESTING = False
    SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@127.0.0.1/flask-test'
    WTF_CSRF_ENABLED = False


class Production(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@127.0.0.1/flask-pro'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}
