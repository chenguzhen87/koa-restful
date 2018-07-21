from flask import Blueprint, g
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from app.apis.models.system_mgr.sysmgr import UserInfo, UserRole, DptInfo, RoleInfo, MenuInfo, RolePermission, OperInfo
from app.apis.utils.common import getSysDateTime
from app.apis.utils.log_helper import mylog
from app.apis.utils.request_helper import MyRequest
from app.apis.utils.response_helper import MyResponse, ResState
from app.apis.utils.sqlalchemy_helper import MySqlalchemy
from app.apis.views.views import login_required, oper_logger
from ext import db_session

system_mgr_user = Blueprint('system_mgr_user', __name__, url_prefix="/system_mgr/user")


##添加
@system_mgr_user.route('/add', methods=['POST'])
@login_required
@oper_logger("添加用户")
def add():
    myRes = MyResponse()
    user = UserInfo()
    user.LOGIN_NAME = MyRequest.get_verify_empty("LOGIN_NAME", errmsg="用户名不能为空")
    user.USER_NAME = MyRequest.get_verify_empty("USER_NAME", errmsg="姓名不能为空")
    user.USER_SEX = MyRequest.get("USER_SEX", type=int)
    user.DPT_KEY = MyRequest.get_verify_empty("DPT_KEY", errmsg="DPT_KEY不能为空")
    user.set_password("123456")
    user.USER_POSITION = MyRequest.get("USER_POSITION", type=str)
    user.PHONE = MyRequest.get("PHONE", type=str)
    user.TIME_CREATE = getSysDateTime()
    user.TIME_MODIFY = getSysDateTime()
    try:
        MySqlalchemy.comAdd(user)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = ResState.ERROR_DB
    return myRes.to_json()


##删除
@system_mgr_user.route('/delete', methods=['DELETE'])
@login_required
@oper_logger("删除用户")
def delete():
    myRes = MyResponse()
    USER_KEY = MyRequest.get("USER_KEY", type=int)
    try:
        MySqlalchemy.comDel(UserInfo, [UserInfo.USER_KEY == USER_KEY])
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = ResState.ERROR_DB
    return myRes.to_json()


##修改用户
@system_mgr_user.route('/update', methods=['POST'])
@login_required
@oper_logger("修改用户")
def update():
    myRes = MyResponse()
    USER_KEY = MyRequest.get("USER_KEY", type=int)
    upd_attr = {}
    upd_attr["USER_NAME"] = MyRequest.get_verify_empty("USER_NAME", errmsg="姓名不能为空")
    upd_attr["USER_SEX"] = MyRequest.get("USER_SEX", type=int, default=1)
    upd_attr["DPT_KEY"] = MyRequest.get_verify_empty("DPT_KEY", errmsg="部门ID不能为空")
    upd_attr["USER_POSITION"] = MyRequest.get("USER_POSITION", type=str)
    upd_attr["PHONE"] = MyRequest.get("PHONE", type=str)
    upd_attr["TIME_MODIFY"] = getSysDateTime()
    try:
        MySqlalchemy.comUpdate(UserInfo, [UserInfo.USER_KEY == USER_KEY], upd_attr)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()


##修改个人基本信息
@system_mgr_user.route('/updMyInfo', methods=['POST'])
@login_required
@oper_logger("修改个人基本信息")
def updMyInfo():
    myRes = MyResponse()
    USER_KEY = g.USER_KEY
    upd_attr = {}
    upd_attr["USER_NAME"] = MyRequest.get_verify_empty("USER_NAME", errmsg="姓名不能为空")
    upd_attr["PHONE"] = MyRequest.get("PHONE", type=str)
    try:
        MySqlalchemy.comUpdate(UserInfo, [UserInfo.USER_KEY == USER_KEY], upd_attr)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    finally:
        db_session.close()
    return myRes.to_json()


##管理员重置用户密码
@system_mgr_user.route('/resetPwdByUserKey', methods=['GET'])
@login_required
@oper_logger("重置密码")
def resetPwdByUserKey():
    myRes = MyResponse()
    USER_KEY = MyRequest.get("USER_KEY", type=int)
    try:
        q_model = db_session.query(UserInfo).filter(UserInfo.USER_KEY == USER_KEY).one()
        q_model.set_password("123456")
        db_session.commit()
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    finally:
        db_session.close()
    return myRes.to_json()


##用户修改自己的密码
@system_mgr_user.route('/resetMyPwd', methods=['POST'])
@login_required
def resetMyPwd():
    myRes = MyResponse()
    FuserId = g.USER_KEY
    FoldPwd = MyRequest.get_verify_empty("FoldPwd", errmsg="旧密码不能为空")
    FnewPwd = MyRequest.get_verify_empty("FnewPwd", errmsg="新密码不能为空")
    FnewPwdOk = MyRequest.get("FnewPwdOk", type=str)
    try:
        if FnewPwd != FnewPwdOk:
            return myRes.to_json_msg("新旧密码不一致")
        userInfo = db_session.query(UserInfo).filter(UserInfo.USER_KEY == FuserId).one()
        if not userInfo.check_password(userInfo.USER_PWD, FoldPwd):
            return myRes.to_json_msg("旧密码错误，请重新输入")
        userInfo.set_password(FnewPwd)
        db_session.commit()
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    finally:
        db_session.close()
    return myRes.to_json()


##修改用户角色
@system_mgr_user.route('/updUserRole', methods=['GET'])
@login_required
@oper_logger("修改用户角色")
def updUserRole():
    myRes = MyResponse()
    ROLE_KEYS = MyRequest.getList("ROLE_KEYS[]")
    USER_KEY = MyRequest.get("USER_KEY", type=int)
    try:
        db_session.begin_nested()
        db_session.query(UserRole).filter(UserRole.USER_KEY == USER_KEY).delete()
        for key in ROLE_KEYS:
            userRole = UserRole()
            userRole.USER_KEY = USER_KEY
            userRole.ROLE_KEY = key
            db_session.add(userRole)
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


@system_mgr_user.route('/getRoleListByUserKey', methods=['GET'])
@login_required
def getRoleListByUserKey():
    myRes = MyResponse()
    USER_KEY = MyRequest.get("USER_KEY", type=int)
    try:
        clomns = [UserRole.USER_KEY, RoleInfo.ROLE_NAME, UserRole.ROLE_KEY]
        query_data = db_session.query(*clomns).outerjoin(RoleInfo, RoleInfo.ROLE_KEY == UserRole.ROLE_KEY).filter(
            UserRole.USER_KEY == USER_KEY)
        myRes.data = MySqlalchemy.convertToList(query_data)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()


##获取人员列表
@system_mgr_user.route('/getList', methods=['GET'])
@login_required
def getList():
    myRes = MyResponse()
    try:
        query_data = db_session.query(UserInfo).all()
        myRes.data = MySqlalchemy.convertToList(query_data)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()


##获取部门人员树
@system_mgr_user.route('/getDptAndUserList', methods=['GET'])
@login_required
def getDptAndUserList():
    myRes = MyResponse()
    try:
        query_data_dpt = db_session.query(DptInfo.DPT_KEY, DptInfo.DPT_PKEY, DptInfo.DPT_NAME)
        query_data_user = db_session.query(UserInfo.USER_KEY, UserInfo.DPT_KEY, UserInfo.USER_NAME).filter(
            UserInfo.USER_KEY != 1)
        query_data = query_data_dpt.union_all(query_data_user)
        myRes.data = MySqlalchemy.convertToList(query_data)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()


###根据id获取用户详细信息
@system_mgr_user.route('/getDetail', methods=['GET'])
@login_required
def getDetail():
    myRes = MyResponse()
    USER_KEY = MyRequest.get("USER_KEY", type=int)
    try:
        columns = [UserInfo.USER_KEY, UserInfo.DPT_KEY, UserInfo.USER_NAME, UserInfo.LOGIN_NAME, UserInfo.USER_SEX,
                   UserInfo.USER_POSITION, UserInfo.PHONE, UserInfo.TIME_CREATE, UserRole.ROLE_KEY]
        dict_user = MySqlalchemy.get_detail(columns, outerjoins=[UserRole, UserRole.USER_KEY == UserInfo.USER_KEY],
                                            filters=[UserInfo.USER_KEY == USER_KEY])
        myRes.code = ResState.HTTP_SUCCESS
        myRes.data = dict_user
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()


###分页查询
@system_mgr_user.route('/getPageList', methods=['GET'])
@login_required
def getPageList():
    myRes = MyResponse()
    currentPage = MyRequest.get("currentPage", type=int)
    pageSize = MyRequest.get("pageSize", type=int)
    searchDptKey = MyRequest.get("searchDptKey", type=str)
    searchName = MyRequest.get("searchName", type=str).strip()
    columns = [UserInfo.USER_KEY, UserInfo.USER_NAME, UserInfo.LOGIN_NAME, UserInfo.USER_SEX, UserInfo.USER_POSITION,
               UserInfo.DPT_KEY, DptInfo.DPT_NAME, UserInfo.TIME_MODIFY, UserInfo.PHONE]
    filters = []
    outerjoins = [(DptInfo, DptInfo.DPT_KEY == UserInfo.DPT_KEY)]
    try:
        USER_KEY = g.USER_KEY
        if USER_KEY != 1:
            filters.append(UserInfo.USER_KEY != 1)
        if searchDptKey != 0:
            filters.append(UserInfo.DPT_KEY.like(searchDptKey + "%"))
        if searchName is not None:
            filters.append(UserInfo.USER_NAME.like("%" + searchName + "%"))
        user_page_info = MySqlalchemy.get_page_list(currentPage, pageSize, UserInfo.USER_KEY, columns,
                                                    outerjoins=outerjoins, filters=filters,
                                                    orders=[UserInfo.TIME_MODIFY.desc()])
        ###拼接用户角色
        query_data_role = db_session.query(UserRole.USER_KEY, RoleInfo.ROLE_NAME, UserRole.ROLE_KEY).outerjoin(RoleInfo,
                                                                                                               RoleInfo.ROLE_KEY == UserRole.ROLE_KEY)
        list_role = MySqlalchemy.convertToList(query_data_role)
        for xuser in user_page_info["data"]:
            list_roleName = []
            for xrole in list_role:
                if xuser["USER_KEY"] == xrole["USER_KEY"]:
                    list_roleName.append(xrole["ROLE_NAME"])
            xuser["ROLE_NAMES"] = ",".join(list_roleName)
        myRes.data = user_page_info
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()


###获取登录用户的菜单列表
@system_mgr_user.route('/getLoginUserPermissionList', methods=['GET'])
@login_required
def getLoginUserPermissionList():
    myRes = MyResponse()
    try:
        USER_KEY = g.USER_KEY
        outerjoins_menu = []
        outerjoins_oper = []
        filters = []
        columns_menu = [MenuInfo.MENU_SOFT, MenuInfo.MENU_KEY, MenuInfo.MENU_ICON, MenuInfo.MENU_URL,
                        MenuInfo.MENU_PKEY, MenuInfo.MENU_NAME]
        columns_oper = [OperInfo.OPER_NAME, OperInfo.OPER_URL]
        if USER_KEY != 12:
            outerjoins_menu = [(RolePermission, and_(MenuInfo.MENU_KEY == RolePermission.RESOURCE_KEY,
                                                     RolePermission.RESOURCE_TYPE == 0)),
                               (UserRole, UserRole.ROLE_KEY == RolePermission.ROLE_KEY)]
            outerjoins_oper = [(RolePermission, and_(OperInfo.OPER_KEY == RolePermission.RESOURCE_KEY,
                                                     RolePermission.RESOURCE_TYPE == 1)), (UserRole,
                                                                                           UserRole.ROLE_KEY == RolePermission.ROLE_KEY)]
            filters = [(UserRole.USER_KEY == USER_KEY)]
        query_data_menu = MySqlalchemy.get_all(columns_menu, outerjoins=outerjoins_menu, filters=filters,
                                               orders=[(MenuInfo.MENU_SOFT.asc())])
        query_data_oper = MySqlalchemy.get_all(columns_oper, outerjoins=outerjoins_oper, filters=filters,
                                               orders=[(OperInfo.OPER_SOFT.asc())])
        myRes.data = {"menuList": query_data_menu, "operList": query_data_oper}
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = str(ex)
    return myRes.to_json()
