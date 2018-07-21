import jwt, datetime, time
import sys
from flask import abort
import app
from app.apis.models.system_mgr.sysmgr import UserInfo
from app.apis.utils.sqlalchemy_helper import MySqlalchemy
from ext import db_session


class Auth(object):
    """
    权限校验、token帮助类
    """
    def __encode_auth_token(self,USER_KEY, login_time):
        """
        生成认证Token
        :param USER_KEY: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            ##exp: 过期时间
            ##nbf: 表示当前时间在nbf里的时间之前，则Token不被接受
            ##iss: token签发者
            ##aud: 接收者
            ##iat: 发行时间
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),
                'iat': datetime.datetime.utcnow(),
                'iss': 'ken',
                'data': {
                    'USER_KEY': USER_KEY,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                app.Config.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e


    def __decode_auth_token(self,auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            ###十分钟无访问token过期
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, app.Config.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload and 'USER_KEY' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'
        except TypeError:
            return '无效Token'
        except:
            print(sys.exc_info()[1])

    @classmethod
    def authenticate(cls,username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        userInfo=db_session.query(UserInfo).filter(UserInfo.LOGIN_NAME==username).first()
        if (userInfo is None):
            return abort(401,"用户名或密码错误")
        else:
            if (userInfo.check_password(userInfo.USER_PWD, password)):
                login_time = int(time.time())
                ###这里后期需要将登录时间写入缓存，提高性能
                token = cls.__encode_auth_token(cls,userInfo.USER_KEY, login_time)
                dict_user=MySqlalchemy.convertToDict(userInfo)
                return dict_user,token.decode()
            else:
                return abort(401, "用户名或密码错误")

    @classmethod
    def identify(cls,request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if (auth_header):
            auth_tokenArr = auth_header.split(" ")
            if (not auth_tokenArr or auth_tokenArr[0] != 'Bearer' or len(auth_tokenArr) != 2):
                abort(401, 'Token错误或已过期，请重新登录')
            else:
                auth_token = auth_tokenArr[1]
                payload = cls.__decode_auth_token(cls,auth_token)
                if not isinstance(payload, str):
                    userInfo = db_session.query(UserInfo).filter(UserInfo.USER_KEY==payload['data']['USER_KEY'])
                    if (userInfo is None):
                        abort(401, '找不到该用户信息')
                    else:
                        # if (user.login_time == payload['data']['login_time']):
                        if True:
                            return payload['data']['USER_KEY']
                        else:
                            abort(401, 'Token已更改，请重新登录获取')
                else:
                    abort(401,  'Token错误或已过期，请重新登录')
        else:
            abort(401,'没有提供认证token')
