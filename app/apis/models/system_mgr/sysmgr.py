from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db

class DptInfo(db.Model):
    __tablename__ = 'DPTINFO'
    DPT_KEY = Column(String(64), primary_key=True,nullable=False)
    DPT_NAME = Column(String(64))
    DPT_PKEY = Column(String(64))
    DPT_SOFT = Column(Integer)

class UserInfo(db.Model):
    __tablename__ = 'USERINFO'
    USER_KEY = Column(Integer, primary_key=True,autoincrement=True,nullable=False)
    DPT_KEY = Column(String(64), ForeignKey('DPTINFO.DPT_KEY'))
    USER_NAME = Column(String(64))
    LOGIN_NAME = Column(String(64),unique=True)
    USER_PWD = Column(String(64))
    USER_SEX = Column(Integer)
    USER_POSITION = Column(String)
    PHONE = Column(String(11))
    TIME_CREATE=Column(DECIMAL(10,7))
    TIME_MODIFY = Column(DECIMAL(10,7))

    def set_password(self, password):
        self.USER_PWD = generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

class RoleInfo(db.Model):
    __tablename__ = 'ROLEINFO'
    ROLE_KEY = Column(Integer, primary_key=True,autoincrement=True,nullable=False)
    ROLE_NAME = Column(String(64))
    DESCRIPT = Column(String(640))
    TIME_CREATE = Column(DECIMAL(10, 7))
    TIME_MODIFY = Column(DECIMAL(10, 7))

class UserRole(db.Model):
    __tablename__ = 'USER_ROLE'
    USER_ROLE_KEY = Column(Integer, primary_key=True,autoincrement=True,nullable=False)
    USER_KEY = Column(Integer,ForeignKey('USERINFO.USER_KEY', ondelete='CASCADE'))
    ROLE_KEY = Column(Integer,ForeignKey('ROLEINFO.ROLE_KEY', ondelete='CASCADE'))

class RolePermission(db.Model):
    __tablename__ = 'ROLE_PERMISSION'
    ROLE_PMS_KEY = Column(Integer, primary_key=True,autoincrement=True,nullable=False)
    ROLE_KEY = Column(Integer, ForeignKey('ROLEINFO.ROLE_KEY', ondelete='CASCADE'))
    RESOURCE_KEY = Column(String(64))
    RESOURCE_TYPE = Column(Integer)

class MenuInfo(db.Model):
    __tablename__ = 'MENUINFO'
    MENU_KEY = Column(String(64), primary_key=True,nullable=False)
    MENU_NAME = Column(String(64))
    MENU_PKEY = Column(String(64))
    MENU_URL = Column(String(64))
    MENU_ICON=Column(String(64))
    MENU_SOFT = Column(String(10),default=1)

class OperInfo(db.Model):
    __tablename__ = 'OPERINFO'
    OPER_KEY = Column(String(64), primary_key=True,nullable=False)
    OPER_NAME = Column(String(64))
    OPER_PKEY = Column(String(64))
    OPER_URL = Column(String(64))
    OPER_TYPE = Column(Integer,default=0)
    OPER_SOFT = Column(Integer,default=1)