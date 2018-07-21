import datetime
import os
import flask
import sys
from werkzeug.utils import secure_filename
from app.apis.utils.log_helper import mylog

class UploadFile(object):
    """
    上传文件帮助类
    """
    def __init__(self,f,sub_dir=None):
        """
        默认构造方法
        :param f: 上传的文件
        :param sub_dir:上传的子路径 /static/...
        """
        self.file = f
        self.sub_dir=sub_dir
        self.filepath=None
        self.filename=None

    def __allowed_file(self,filename):
        """
        私有方法，负责校验上传文件是否符合要求
        :param filename:
        :return:
        """
        ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])
        return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

    def __upload(self,filepath):
        """
        真是的上传方法
        :param filepath:
        :return:
        """

        if self.file:  # 判断是否为None
            try:
                fname = secure_filename(self.file.filename)
                str_now_time=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                new_filename = str_now_time + '_' + fname  # 修改了上传的文件名
                self.file.save(os.path.join(filepath, new_filename))
                self.filepath=filepath
                self.filename=new_filename
            except:
                mylog.error(sys.exc_info()[1])
                flask.abort(400,sys.exc_info()[1])

    def upload_single_file(self):
        """
        上传单个文件
        :return:
        """
        from config import Config
        relative_path= os.path.join(Config.UPLOAD_PATH,self.sub_dir)
        ###判断文件夹是否存在，不存在则创建
        if not os.path.exists(relative_path):
            os.makedirs(relative_path)
        self.__upload(relative_path)

    def import_file(self):
        """
        导入文件上传，先上船到指定位置，在做读取操作
        :return:
        """
        from config import Config
        relative_path = Config.EXPORT_PATH
        ###判断文件夹是否存在，不存在则创建
        if not os.path.exists(relative_path):
            os.makedirs(relative_path)
        self.__upload(relative_path)