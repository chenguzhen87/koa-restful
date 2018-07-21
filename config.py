import os
basedir = os.path.abspath(os.path.dirname(__file__))  

class Config(object):

    DEBUG = False
    TESTING = False
    SECRET_KEY = 'ATS-WEB'

    ###SQLALCHEMY
    ###如果设置成 True，SQLAlchemy 将会记录所有 发到标准输出(stderr)的语句，这对调试很有帮助。
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://devuser:root@192.168.1.60:3306/testdb?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///' + os.path.join(basedir, 'db/ats.db')

    ###flask-session
    SESSION_TYPE='null'
    SESSION_KEY_PREFIX="session:"
    ########如果设置为True的话，session的生命为 permanent_session_lifetime 秒（默认是31天）
    ########如果设置为Flase的话，那么当用户关闭浏览器时，session便被删除了。permanent_session_lifetime也会生效
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 31
    #SESSION_REDIS=redis.Redis(host="127.0.0.1",port="6379")

    ###导出office路径
    EXPORT_PATH = "/static/exports"
    IMPORT_PATH = "/static/import"
    UPLOAD_PATH = "/static/uploads"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DB_CONFIG = {'host': '192.168.1.60', 'port': 3306, 'user': 'devuser', 'password': 'root', 'db': 'data',
                 'connect_timeout': 300, 'read_timeout': 300, 'write_timeout': 300,
                 'charset': 'utf8'}
    pass

class TestingConfig(Config):
    TESTING = False
    DB_CONFIG = {'host': '192.168.1.60', 'port': 3306, 'user': 'devuser', 'password': 'root', 'db': 'data',
                 'connect_timeout': 300, 'read_timeout': 300, 'write_timeout': 300,
                 'charset': 'utf8'}
    pass

class ProductionConfig(Config):
    DEBUG = False
    DB_CONFIG = {'host': '192.168.1.60', 'port': 3306, 'user': 'devuser', 'password': 'root', 'db': 'data',
                 'connect_timeout': 300, 'read_timeout': 300, 'write_timeout': 300,
                 'charset': 'utf8'}
    pass

config={
        'development':DevelopmentConfig,
        'testing':TestingConfig,
        'production':ProductionConfig,
        'default':DevelopmentConfig
        }
