from flask import Blueprint, g
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from app.apis.models.system_mgr.sysmgr import MenuInfo, UserRole, RolePermission
from app.apis.utils.log_helper import mylog
from app.apis.utils.request_helper import MyRequest
from app.apis.utils.response_helper import MyResponse, ResState
from app.apis.utils.sqlalchemy_helper import MySqlalchemy
from app.apis.views.views import oper_logger, login_required, login_super
from ext import db_session

system_mgr_menu = Blueprint('system_mgr_menu', __name__, url_prefix="/system_mgr/menu")

##添加菜单
@system_mgr_menu.route('/add', methods=['POST'])
@login_required
@oper_logger("添加菜单")
def add():
    myRes = MyResponse()
    MENU_NAME = MyRequest.get_verify_empty("MENU_NAME", errmsg="菜单名称不能为空")
    MENU_PKEY = MyRequest.get_verify_empty("MENU_PKEY", errmsg="MENU_PKEY")
    MENU_URL = MyRequest.get("MENU_URL", type=str)
    MENU_ICON = MyRequest.get("MENU_ICON", type=str)
    MENU_SOFT = MyRequest.get("MENU_SOFT", type=str)
    try:
        mybrother = db_session.query(MenuInfo.MENU_KEY).filter(MenuInfo.MENU_PKEY == MENU_PKEY).all()
        if mybrother:
            array_id = [int(x.MENU_KEY) for x in mybrother]
            ###取最大的ID
            MENU_KEY = str(max(array_id) + 1)
        elif MENU_PKEY == "0":
            MENU_KEY = "101"
        else:
            MENU_KEY = MENU_PKEY + "001"
        menu = MenuInfo()
        menu.MENU_KEY = MENU_KEY
        menu.MENU_NAME = MENU_NAME
        menu.MENU_PKEY = MENU_PKEY
        menu.MENU_URL = MENU_URL
        menu.MENU_ICON = MENU_ICON
        menu.MENU_SOFT = MENU_SOFT
        MySqlalchemy.comAdd(menu)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()

##删除菜单
@system_mgr_menu.route('/delete', methods=['DELETE'])
@login_required
@oper_logger("删除菜单")
def delete():
    myRes = MyResponse()
    MENU_KEY = MyRequest.get_verify_empty("MENU_KEY", errmsg="Fid不能为空")
    try:
        db_session.begin_nested()
        ###删除角色与权限关联信息
        db_session.query(RolePermission).filter(RolePermission.RESOURCE_TYPE == 0).filter(RolePermission.RESOURCE_KEY.like(MENU_KEY+"%")).delete(synchronize_session=False)
        ###删除菜单
        db_session.query(MenuInfo).filter(MenuInfo.MENU_KEY.like(MENU_KEY+"%")).delete(synchronize_session=False)
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
@system_mgr_menu.route('/update', methods=['POST'])
@login_required
@login_super
@oper_logger("修改菜单")
def update():
    myRes = MyResponse()
    MENU_KEY = MyRequest.get_verify_empty("MENU_KEY", errmsg="MENU_KEY不能为空")
    menu_attrs = {}
    menu_attrs["MENU_NAME"] = MyRequest.get("MENU_NAME", type=str)
    menu_attrs["MENU_URL"] = MyRequest.get("MENU_URL", type=str)
    menu_attrs["MENU_ICON"] = MyRequest.get("MENU_ICON", type=str)
    menu_attrs["MENU_SOFT"] = MyRequest.get("MENU_SOFT", type=str)
    try:
        MySqlalchemy.comUpdate(MenuInfo, [MenuInfo.MENU_KEY==MENU_KEY], menu_attrs)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()

###根据菜单id获取功能详细信息，报货菜单按钮列表
@system_mgr_menu.route('/getDetail', methods=['GET'])
@login_required
def getDetail():
    myRes = MyResponse()
    Fid = MyRequest.get_verify_empty("Fid", errmsg="Fid不能为空")
    try:
        query_menu=db_session.query(MenuInfo).filter(MenuInfo.Fid==Fid).one()
        dict_menu=MySqlalchemy.convertToDict(query_menu)
        myRes.data = dict_menu
        myRes.code = ResState.HTTP_SUCCESS
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()

#获取所有的菜单
@system_mgr_menu.route('/getList', methods=['GET'])
@login_required
def getList():
    myRes = MyResponse()
    try:
        query_menu = db_session.query(MenuInfo.MENU_KEY, MenuInfo.MENU_PKEY, MenuInfo.MENU_NAME,MenuInfo.MENU_URL,MenuInfo.MENU_ICON,MenuInfo.MENU_SOFT).order_by(MenuInfo.MENU_SOFT.asc()).all()
        myRes.data=MySqlalchemy.convertToList(query_menu)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()