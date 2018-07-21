from flask import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from app.apis.models.system_mgr.sysmgr import RoleInfo, RolePermission
from app.apis.utils.common import getSysDateTime
from app.apis.utils.exception_helper import MyError
from app.apis.utils.log_helper import mylog
from app.apis.utils.request_helper import MyRequest
from app.apis.utils.response_helper import MyResponse, ResState
from app.apis.utils.sqlalchemy_helper import MySqlalchemy
from app.apis.views.views import login_required, oper_logger
from ext import db_session
from flask import request

system_mgr_role = Blueprint('system_mgr_role', __name__, url_prefix="/system_mgr/role")

##添加
@system_mgr_role.route('/add', methods=['POST'])
@login_required
@oper_logger("添加角色")
def add():
    myRes = MyResponse()
    ROLE_NAME = MyRequest.get_verify_empty("ROLE_NAME")
    DESCRIPT = MyRequest.get("DESCRIPT")
    try:
        role = RoleInfo()
        role.ROLE_NAME = ROLE_NAME
        role.DESCRIPT = DESCRIPT
        role.TIME_CREATE = getSysDateTime()
        role.TIME_MODIFY = getSysDateTime()
        MySqlalchemy.comAdd(role)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except MyError as ex:
        myRes.msg = ex
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = ResState.ERROR_DB
    return myRes.to_json()

##删除
@system_mgr_role.route('/delete', methods=['DELETE'])
@login_required
@oper_logger("删除角色")
def delete():
    myRes = MyResponse()
    ROLE_KEY = MyRequest.get("ROLE_KEY", type=int)
    try:
        MySqlalchemy.comDel(RoleInfo,[RoleInfo.ROLE_KEY==ROLE_KEY])
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        db_session.rollback()
        mylog.error(ex)
        myRes.msg = str(ex)
    finally:
        db_session.close()
    return myRes.to_json()

##修改角色
@system_mgr_role.route('/update', methods=['POST'])
@login_required
@oper_logger("修改角色")
def update():
    myRes = MyResponse()
    ROLE_KEY = MyRequest.get("ROLE_KEY", type=int)
    role_attrs={}
    role_attrs["ROLE_NAME"] = MyRequest.get_verify_empty("ROLE_NAME")
    role_attrs["DESCRIPT"] = MyRequest.get("DESCRIPT")
    role_attrs["TIME_MODIFY"] = getSysDateTime()
    try:
        MySqlalchemy.comUpdate(RoleInfo,[RoleInfo.ROLE_KEY==ROLE_KEY],role_attrs)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()

###根据id获取角色详细信息
@system_mgr_role.route('/getDetail', methods=['GET'])
@login_required
def getDetail():
    myRes = MyResponse()
    ROLE_KEY = MyRequest.get("ROLE_KEY", type=int)
    try:
        query_data=db_session.query(RoleInfo).filter(RoleInfo.ROLE_KEY==ROLE_KEY).one()
        dict_data=MySqlalchemy.convertToDict(query_data)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.data = dict_data
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()

@system_mgr_role.route('/getList', methods=['GET'])
@login_required
def getList():
    myRes = MyResponse()
    try:
        query_data = db_session.query(RoleInfo).order_by(RoleInfo.TIME_MODIFY.desc())
        myRes.data=MySqlalchemy.convertToList(query_data)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()

##修改角色权限
@system_mgr_role.route('/updRolePermission', methods=['GET'])
@login_required
@oper_logger("修改角色权限")
def updRolePermission():
    myRes = MyResponse()
    RESOURCE_KEYS = MyRequest.get_verify_list("RESOURCE_KEYS")
    ROLE_KEY = MyRequest.get("ROLE_KEY", type=int)
    RESOURCE_TYPE = MyRequest.get("RESOURCE_TYPE", type=int)
    try:
        db_session.begin_nested()
        db_session.query(RolePermission).filter(RolePermission.ROLE_KEY == ROLE_KEY).filter(RolePermission.RESOURCE_TYPE==RESOURCE_TYPE).delete(synchronize_session=False)
        for key in RESOURCE_KEYS:
            rolePermission = RolePermission()
            rolePermission.ROLE_KEY=ROLE_KEY
            rolePermission.RESOURCE_KEY=key
            rolePermission.RESOURCE_TYPE=RESOURCE_TYPE
            db_session.add(rolePermission)
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

#获取角色的菜单列表
@system_mgr_role.route('/getRoleMenuAndOperList', methods=['GET'])
@login_required
def getRoleMenuAndOperList():
    myRes = MyResponse()
    ROLE_KEY = MyRequest.get("ROLE_KEY", type=int)
    try:
        query_data = db_session.query(RolePermission.ROLE_KEY,RolePermission.RESOURCE_KEY,RolePermission.RESOURCE_TYPE).filter(RolePermission.ROLE_KEY==ROLE_KEY)
        myRes.data=MySqlalchemy.convertToList(query_data)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()