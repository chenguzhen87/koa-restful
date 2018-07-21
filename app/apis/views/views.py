import json
from functools import wraps
import sys
import os
from app.apis.models.system_monitor.system_monitor import LogOper, LogLogin
from flask import request, abort, g, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from app.apis.utils.auth_helper import Auth
from app.apis.utils.common import getSysDateTime
from app.apis.utils.log_helper import mylog
from app.apis.utils.request_helper import MyRequest
from app.apis.utils.response_helper import ResState, MyResponse, DownLoadFile
from app.apis.utils.sqlalchemy_helper import MySqlalchemy

main = Blueprint('apis',__name__)
###########记录操作日志
def oper_logger(oper_descript=""):
    def _oper_logger(func):
        @wraps(func)
        def wrapper(*args,**kargs):
            responseInfo = func()
            ###操作成功后，记录操作日志
            if json.loads(responseInfo.data)["code"]==ResState.HTTP_SUCCESS:
                try:
                    logOper = LogOper()
                    logOper.USER_KEY = g.USER_KEY
                    logOper.IP_ADDRESS = request.remote_addr
                    logOper.LOGO_FUNC = "function(name=%s,args=%s,kargs=%s)" % (func.__name__, args, kargs)
                    logOper.LOGO_REQ_PARAMS = json.dumps(MyRequest.getAll())
                    logOper.TIME_CREATE=getSysDateTime()
                    logOper.DESCRIPT=oper_descript
                    try:
                        MySqlalchemy.comAdd(logOper)
                    except SQLAlchemyError as ex:
                        mylog.error(ex)
                except:
                    print(sys.exc_info())
                    pass
            return responseInfo
        return wrapper
    return _oper_logger

###########记录登录日志
def login_logger(oper_descript=""):
    logLogin = LogLogin()
    logLogin.USER_KEY = g.FuserId
    logLogin.IP_ADDRESS = request.remote_addr
    logLogin.TIME_CREATE = getSysDateTime()
    logLogin.DESCRIPT = oper_descript
    try:
        MySqlalchemy.comAdd(logLogin)
    except SQLAlchemyError as ex:
        mylog.error(ex)

###登录
@main.route('/login', methods=['POST'])
def login():
    myRes = MyResponse()
    try:
        FloginName = MyRequest.get_verify_empty("FloginName", errmsg="用户名不能为空")
        Fpwd = MyRequest.get_verify_empty("Fpwd", errmsg="密码不能为空")
        from app.apis.utils.auth_helper import Auth
        dict_user, token = Auth.authenticate(FloginName, Fpwd)
        userInfo={"USER_NAME":dict_user["USER_NAME"],"LOGIN_NAME":dict_user["LOGIN_NAME"],"PHONE":dict_user["PHONE"]}
        g.FuserId = dict_user["USER_KEY"]
        myRes.data = {"userInfo": userInfo, "token": token}
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "登录成功"
        login_logger("用户登录")
    except SQLAlchemyError as ex:
        mylog.error(ex)
        return myRes.to_json_msg(ResState.ERROR_DB)
    return myRes.to_json()

###登录校验装饰器
def login_required(func):
    @wraps(func)
    def wrapper():
        USER_KEY = Auth.identify(request)
        if USER_KEY>0:
            g.USER_KEY=USER_KEY
            ###token验证，服务于restful
            return func()
        else:
            abort(401)
    return wrapper

###权限验证装饰器
def login_super(func):
    @wraps(func)
    def wrapper():
        if g.USER_KEY!=1:
            abort(403)
        return func()
    return wrapper

#退出登录
@main.route("/logout", methods=['GET'])
@login_required
def logout():
    myRes = MyResponse()
    login_logger("退出登录")
    myRes.code = ResState.HTTP_SUCCESS
    myRes.msg = "操作成功"
    return myRes.to_json()

@main.route("/download", methods=['GET'])
def download():
    downLoadFile = DownLoadFile()
    file=MyRequest.get("filepath",type=str)
    filename = os.path.basename(file)
    filepath = os.path.dirname(file)
    downLoadFile.filepath = filepath
    downLoadFile.filename = filename
    downLoadFile.newfilename = filename.split("_")[1]
    return downLoadFile.download()


