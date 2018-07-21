from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from ext import db

class LogLogin(db.Model):
    __tablename__ = 'LOG_LOGIN'
    LOGL_KEY = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    USER_KEY = Column(Integer)
    IP_ADDRESS = Column(String(15))
    TIME_CREATE = Column(DECIMAL(16, 6))
    DESCRIPT = Column(String(640))

class LogOper(db.Model):
    __tablename__ = 'LOG_OPER'
    LOGO_KEY = Column(Integer, primary_key=True, autoincrement=True,nullable=False)
    USER_KEY = Column(Integer)
    IP_ADDRESS = Column(String(15))
    LOGO_FUNC = Column(String(64))
    LOGO_REQ_PARAMS = Column(String(1280))
    TIME_CREATE = Column(DECIMAL(16, 6))
    DESCRIPT = Column(String(640))