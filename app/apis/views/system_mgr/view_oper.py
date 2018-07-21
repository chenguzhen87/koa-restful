from flask import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from app.apis.models.system_mgr.sysmgr import RolePermission, OperInfo
from app.apis.utils.log_helper import mylog
from app.apis.utils.request_helper import MyRequest
from app.apis.utils.response_helper import MyResponse, ResState
from app.apis.utils.sqlalchemy_helper import MySqlalchemy
from app.apis.views.views import oper_logger, login_required, login_super
from ext import db_session

system_mgr_oper = Blueprint('system_mgr_oper', __name__, url_prefix="/system_mgr/oper")

##添加菜单按钮
@system_mgr_oper.route('/add', methods=['POST'])
@login_required
@login_super
@oper_logger("添加操作")
def add():
    myRes = MyResponse()
    OPER_NAME = MyRequest.get_verify_empty("OPER_NAME", errmsg="操作名称不能为空")
    OPER_PKEY = MyRequest.get_verify_empty("OPER_PKEY", errmsg="OPER_PKEY不能为空")
    OPER_URL = MyRequest.get("OPER_URL", type=str)
    OPER_TYPE = MyRequest.get("OPER_TYPE", type=int)
    OPER_SOFT = MyRequest.get("OPER_SOFT", type=int)
    try:
        mybrother = db_session.query(OperInfo.OPER_KEY).filter(OperInfo.OPER_PKEY == OPER_PKEY).all()
        if mybrother:
            array_id = [int(x.OPER_KEY) for x in mybrother]
            ###取最大的ID
            OPER_KEY = str(max(array_id) + 1)
        elif OPER_PKEY == "0":
            OPER_KEY = "101"
        else:
            OPER_KEY = OPER_PKEY + "001"
        operInfo = OperInfo()
        operInfo.OPER_KEY = OPER_KEY
        operInfo.OPER_NAME = OPER_NAME
        operInfo.OPER_URL = OPER_URL
        operInfo.OPER_TYPE = OPER_TYPE
        operInfo.OPER_PKEY = OPER_PKEY
        operInfo.OPER_SOFT = OPER_SOFT
        MySqlalchemy.comAdd(operInfo)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()

##删除菜单
@system_mgr_oper.route('/delete', methods=['DELETE'])
@login_required
@login_super
@oper_logger("删除操作")
def delete():
    myRes = MyResponse()
    OPER_KEY = MyRequest.get_verify_empty("OPER_KEY", errmsg="OPER_KEY不能为空")
    try:
        db_session.begin_nested()
        ###删除按钮相关的角色权限信息
        db_session.query(RolePermission).filter(RolePermission.RESOURCE_TYPE == 1).filter(RolePermission.RESOURCE_KEY.like(OPER_KEY+"%")).delete(synchronize_session=False)
        ###删除按钮信息
        db_session.query(OperInfo).filter(OperInfo.OPER_KEY.like(OPER_KEY+"%")).delete(synchronize_session=False)
        db_session.commit()
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        db_session.rollback()
        mylog.error(ex)
        myRes.msg = str(ex)
    finally:
        db_session.close()
    return myRes.to_json()

##修改菜单
@system_mgr_oper.route('/update', methods=['POST'])
@login_required
@login_super
@oper_logger("修改菜单按钮")
def update():
    myRes = MyResponse()
    OPER_KEY = MyRequest.get_verify_empty("OPER_KEY", errmsg="OPER_KEY不能为空")
    oper_attrs = {}
    oper_attrs["OPER_NAME"] = MyRequest.get_verify_empty("OPER_NAME", errmsg="按钮编码不能为空")
    oper_attrs["OPER_URL"] = MyRequest.get("OPER_URL", type=str)
    oper_attrs["OPER_TYPE"] = MyRequest.get("OPER_TYPE", type=int)
    oper_attrs["OPER_SOFT"] = MyRequest.get("OPER_SOFT", type=int)
    try:
        MySqlalchemy.comUpdate(OperInfo, [OperInfo.OPER_KEY==OPER_KEY], oper_attrs)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()

###根据id获取c菜单按钮详细信息
@system_mgr_oper.route('/getDetail', methods=['GET'])
@login_required
def getDetail():
    myRes = MyResponse()
    OPER_KEY = MyRequest.get_verify_empty("OPER_KEY",errmsg="OPER_KEY不能为空")
    try:
        query_data=db_session.query(OperInfo).filter(OperInfo.OPER_KEY==OPER_KEY).one()
        dict_menu=MySqlalchemy.convertToDict(query_data)
        myRes.data = dict_menu
        myRes.code = ResState.HTTP_SUCCESS
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()

#获取所有的菜单
@system_mgr_oper.route('/getList', methods=['GET'])
@login_required
def getList():
    myRes = MyResponse()
    try:
        query_menuButton = db_session.query(OperInfo).order_by(OperInfo.OPER_SOFT.asc()).all()
        myRes.data=MySqlalchemy.convertToList(query_menuButton)
        print(myRes.data)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()