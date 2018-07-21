import sys
import os
import time
import pandas
from app.apis.models.system_mgr.sysmgr import UserInfo
from app.apis.models.system_monitor.system_monitor import LogOper, LogLogin
from flask import request, Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from app.apis.utils.common import getSysDateTime, getSysDateTimeStr, fun_time
from app.apis.utils.ecxel_helper import XlsxwriterWriter, XlrdReader
from app.apis.utils.exception_helper import ExcelError
from app.apis.utils.log_helper import mylog
from app.apis.utils.request_helper import MyRequest
from app.apis.utils.response_helper import DownLoadFile, MyResponse,ResState
from app.apis.utils.sqlalchemy_helper import MySqlalchemy
from app.apis.utils.updown_helper import UploadFile
from app.apis.views.views import login_required
from ext import db_session

system_monitor_log = Blueprint('system_monitor_log', __name__, url_prefix="/system_monitor/log")

###操作日志
@system_monitor_log.route('/getPageListOper', methods=['GET'])
@login_required
def getPageListOper():
    myRes = MyResponse()
    currentPage = MyRequest.get("currentPage", type=int)
    pageSize = MyRequest.get("pageSize", type=int)
    searchName = MyRequest.get("searchName", type=str).strip()
    startDate = MyRequest.get_verify_date("startDate")
    endDate = MyRequest.get_verify_date("endDate")
    try:
        columns=[LogOper.LOGO_KEY, LogOper.LOGO_FUNC, LogOper.LOGO_REQ_PARAMS, LogOper.TIME_CREATE, LogOper.DESCRIPT,LogOper.IP_ADDRESS, UserInfo.LOGIN_NAME, UserInfo.USER_NAME]
        outerjoins=[(UserInfo, UserInfo.USER_KEY == LogOper.USER_KEY)]
        filters=[LogOper.TIME_CREATE.between(startDate, endDate)]
        if searchName!='':
            filters.append(UserInfo.LOGIN_NAME.like("%" + searchName + "%"))
        myRes.data=MySqlalchemy.get_page_list(currentPage,pageSize,LogOper.LOGO_KEY,columns,outerjoins=outerjoins,filters=filters,orders=[LogOper.TIME_CREATE.desc()])
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()

###登入登出日志
@system_monitor_log.route('/getPageListLogin', methods=['GET'])
@login_required
def getPageListLogin():
    myRes = MyResponse()
    currentPage = MyRequest.get("currentPage", type=int)
    pageSize = MyRequest.get("pageSize", type=int)
    searchName = MyRequest.get("searchName", type=str).strip()
    startDate = MyRequest.get_verify_date("startDate")
    endDate = MyRequest.get_verify_date("endDate")
    try:
        columns = [LogLogin.LOGL_KEY, LogLogin.TIME_CREATE, LogLogin.DESCRIPT,LogLogin.IP_ADDRESS, UserInfo.LOGIN_NAME, UserInfo.USER_NAME]
        outerjoins = [(UserInfo, UserInfo.USER_KEY == LogLogin.USER_KEY)]
        filters = [LogLogin.TIME_CREATE.between(startDate, endDate)]
        if searchName != '':
            filters.append(UserInfo.FloginName.like("%" + searchName + "%"))
        myRes.data = MySqlalchemy.get_page_list(currentPage, pageSize, LogLogin.LOGL_KEY, columns, outerjoins=outerjoins,
                                                filters=filters, orders=[LogLogin.TIME_CREATE.desc()])
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except SQLAlchemyError as ex:
        mylog.error(ex)
        myRes.msg=str(ex)
    return myRes.to_json()

###导出登录日志到excel
@system_monitor_log.route('/exportLogLogin',methods=['GET'])
@login_required
def exportLogLogin():
    myRes = MyResponse()
    searchName = MyRequest.get("searchName", type=str).strip()
    startDate = MyRequest.get_verify_date("startDate")
    endDate = MyRequest.get_verify_date("endDate")
    downLoadFile=DownLoadFile()
    xlsxwriterWriter = XlsxwriterWriter()
    try:
        db_query = db_session.query(UserInfo.Fid,UserInfo.FloginName, UserInfo.Fname,LogLogin.FcreateTime, LogLogin.Fremark,
                                    LogLogin.FipAddress)
        db_query = db_query.outerjoin(UserInfo, UserInfo.Fid == LogLogin.FuserId)
        db_query = db_query.filter(LogLogin.FcreateTime.between(startDate, endDate))
        if searchName != '':
            db_query = db_query.filter(UserInfo.FloginName.like("%" + searchName + "%"))
        query_data = db_query.order_by(LogLogin.FcreateTime.desc())
        dataArray = MySqlalchemy.convertToDict(query_data)
        df = pandas.DataFrame(dataArray)
        xlsxwriterWriter.open()
        xlsxwriterWriter.writeSheetbyList(df, titles=None, sheetname="ttt")
        downLoadFile.filepath = xlsxwriterWriter.filepath
        downLoadFile.filename=xlsxwriterWriter.filename
        downLoadFile.newfilename = "操作日志"+getSysDateTimeStr()+".xlsx"
        myRes.data=[]
        myRes.code = ResState.HTTP_SUCCESS
        myRes.msg = "操作成功"
    except ExcelError as ex:
        mylog.error(ex)
        abort(404, "写入excel错误")
    except SQLAlchemyError as ex:
        mylog.error(ex)
        abort(404, sys.exc_info()[1])
    finally:
        xlsxwriterWriter.close()
    return downLoadFile.download()

###导出操作日志到excel
@system_monitor_log.route('/exportLogOper',methods=['GET'])
@login_required
def exportLogOper():
    start_time=time.time()
    searchName = MyRequest.get("searchName", type=str).strip()
    startDate = MyRequest.get_verify_date("startDate")
    endDate = MyRequest.get_verify_date("endDate")
    downLoadFile=DownLoadFile()
    xlsxwriterWriter = XlsxwriterWriter()
    try:
        query_data = db_session.query(LogOper).all()
        from app.apis.utils.thread_helper import convertToListThread
        dataArray=convertToListThread(query_data)
        end_time=time.time()
        print(end_time-start_time)
        print(len(dataArray))
        # df = pandas.DataFrame(dataArray)
        # xlsxwriterWriter.open()
        # xlsxwriterWriter.writeSheetbyList(df, titles=None, sheetname="ttt")
        # downLoadFile.filepath = xlsxwriterWriter.filepath
        # downLoadFile.filename=xlsxwriterWriter.filename
        # downLoadFile.newfilename = "操作日志"+getSysDateTimeStr()+".xlsx"
    except ExcelError as ex:
        mylog.error(ex)
        abort(404, "写入excel错误")
    except SQLAlchemyError as ex:
        mylog.error(ex)
        abort(404, sys.exc_info()[1])
    except Exception as ex:
        mylog.error(ex)
        abort(404, sys.exc_info()[1])
    finally:
        xlsxwriterWriter.close()
    myRes = MyResponse()
    print("ok")
    return myRes.to_json()

###导入登录日志
@system_monitor_log.route('/importLogLogin',methods=['POST'])
@login_required
def importLogLogin():
    myRes=MyResponse()
    try:
        ###添加注入清单信息
        f = request.files['Ffile']
        uploadFile = UploadFile(f)
        uploadFile.import_file()
        xlrdReader=XlrdReader(os.path.join(uploadFile.filepath,uploadFile.filename))
        xlrdReader.readSheetToList()
        reader_data=xlrdReader.datas
        reader_titles=xlrdReader.titles
        for index_row,row in enumerate(reader_data):
            sysLog = LogLogin()
            sysLog.FuserId = row[0]
            sysLog.FcreateTime=getSysDateTime()
            sysLog.Ffunc = row[1]
            sysLog.FipAddress = row[2]
            sysLog.Fremark = row[5]
            db_session.add(sysLog)
        db_session.commit()
        myRes.code=ResState.HTTP_SUCCESS
    except ExcelError as ex:
        mylog.error(ex)
        abort(404, "读取excel错误")
    except SQLAlchemyError as ex:
        db_session.rollback()
        mylog.error(ex)
        abort(404, sys.exc_info()[1])
    finally:
        pass
    return myRes.to_json()