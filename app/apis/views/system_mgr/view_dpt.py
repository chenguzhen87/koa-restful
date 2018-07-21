from flask import Blueprint
from sqlalchemy.exc import SQLAlchemyError
from app.apis.models.system_mgr.sysmgr import DptInfo
from app.apis.utils.log_helper import mylog
from app.apis.utils.request_helper import MyRequest
from app.apis.utils.response_helper import MyResponse, ResState
from app.apis.utils.sqlalchemy_helper import MySqlalchemy
from app.apis.views.views import oper_logger, login_required
from ext import db_session

system_mgr_dpt = Blueprint('system_mgr_dpt', __name__, url_prefix="/system_mgr/dpt")

@system_mgr_dpt.route('/add', methods=['POST'])
@login_required
@oper_logger("添加部门")
def add():
    myRes = MyResponse()
    DPT_PKEY = MyRequest.get_verify_empty("DPT_PKEY", errmsg="请选择一个父节点")
    DPT_NAME = MyRequest.get_verify_empty("DPT_NAME", errmsg="部门名称不能为空")
    DPT_SOFT = MyRequest.get("DPT_SOFT", type=int)
    try:
        mybrother = db_session.query(DptInfo.DPT_KEY).filter(DptInfo.DPT_PKEY == DPT_PKEY).all()
        if mybrother:
            array_id = [int(x.DPT_KEY) for x in mybrother]
            ###取最大的ID
            DPT_KEY = str(max(array_id) + 1)
        elif DPT_PKEY=="0":
            DPT_KEY = "101"
        else:
            DPT_KEY=DPT_PKEY+"001"
        dpt = DptInfo()
        dpt.DPT_KEY=DPT_KEY
        dpt.DPT_PKEY = DPT_PKEY
        dpt.DPT_NAME = DPT_NAME
        dpt.DPT_SOFT = DPT_SOFT
        MySqlalchemy.comAdd(dpt)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=ResState.ERROR_DB
    return myRes.to_json()

##删除
@system_mgr_dpt.route('/delete', methods=['DELETE'])
@login_required
@oper_logger("删除")
def delete():
    myRes = MyResponse()
    DPT_KEY = MyRequest.get_verify_empty("DPT_KEY", errmsg="ID不能为空")
    try:
        rows = db_session.query(DptInfo).filter(DptInfo.DPT_KEY.like(DPT_KEY+"%")).delete(synchronize_session=False)
        db_session.commit()
        if rows < 1:
            raise SQLAlchemyError("操作失败")
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = ResState.ERROR_DB
    finally:
        db_session.close()
    return myRes.to_json()

##修改
@system_mgr_dpt.route('/update', methods=['POST'])
@login_required
@oper_logger("修改")
def update():
    myRes = MyResponse()
    DPT_KEY = MyRequest.get_verify_empty("DPT_KEY", errmsg="ID不能为空")
    upd_attr={}
    upd_attr["DPT_NAME"] = MyRequest.get_verify_empty("DPT_NAME", errmsg="部门名称不能为空")
    upd_attr["DPT_SOFT"] = MyRequest.get("DPT_SOFT", type=int)
    try:
        MySqlalchemy.comUpdate(DptInfo,[DptInfo.DPT_KEY==DPT_KEY],upd_attr)
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = ResState.ERROR_DB
    return myRes.to_json()


#获取所有的功能树
@system_mgr_dpt.route('/getList', methods=['GET'])
@login_required
def getList():
    myRes = MyResponse()
    try:
        myRes.data=MySqlalchemy.get_all(DptInfo,orders=DptInfo.DPT_SOFT.asc())
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg = ResState.ERROR_DB
    return myRes.to_json()

###根据id获取c菜单按钮详细信息
@system_mgr_dpt.route('/getDetail', methods=['GET'])
@login_required
def getDetail():
    myRes = MyResponse()
    DPT_KEY = MyRequest.get_verify_empty("DPT_KEY", errmsg="部门ID不能为空")
    try:
        query_data=db_session.query(DptInfo).filter(DptInfo.DPT_KEY==DPT_KEY).one()
        dict_menu=MySqlalchemy.convertToDict(query_data)
        myRes.data = dict_menu
        myRes.code = ResState.HTTP_SUCCESS
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()


