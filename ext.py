'''
ext.py文件：把db变量放到一个单独的文件，而不是放在主app文件。这样做的目的是为了在大型项目中如果db被多个模型
文件引用的话，会造成from your_app import db这样的方式，但是往往也在your_app.py中也会引入模型文件定义的类，这
就造成了循环引用。所以最好的办法是把它放在不依赖其他模块的独立文件中。
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()
db_session = SQLAlchemy().session

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """
    配置sqlite级联删除
    :param dbapi_connection:
    :param connection_record:
    :return:
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()