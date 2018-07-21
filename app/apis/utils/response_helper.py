import datetime
import json
from flask import Response, send_from_directory


class ResState():
    """
    HTTP状态
    """
    HTTP_SUCCESS = 200
    HTTP_ERROR = 400
    ###提示信息全局变量
    ERROR_MSG = "操作失败"
    ERROR_DB = "操作失败，请与管理员联系或稍后重试"
    ERROR_SYS = "系统错误，请与管理员联系或稍后重试"
    ERROR_PARSE_DATA = "数据解析错误，请与管理员联系或稍后重试"

class MyResponse(object):
    """
    适用于增删改查的返回
    """
    def __init__(self):
        self.code = ResState.HTTP_ERROR
        self.msg = ResState.ERROR_MSG
        self.data = None

    def to_json(self):
        return Response(json.dumps(self.__dict__, ensure_ascii=False,cls=DateEncoder), content_type="application/json")

    def to_json_msg(self,msg):
        self.msg=msg
        return self.to_json()

class DownLoadFile(object):
    """
    下载文件帮助类
    """
    def __init__(self):
        self.filepath=None
        self.filename=None
        self.newfilename=None

    def download(self):
        attachment_filename=self.newfilename.encode().decode('latin-1')
        return send_from_directory(self.filepath,self.filename,as_attachment=True, attachment_filename=attachment_filename)

class DateEncoder(json.JSONEncoder):
    """
    格式化response中的日期
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)



