import os
from flask import Flask, request, g
from flask_cors import CORS
from app.apis import register_app
from app.apis.utils.log_helper import init_log
from config import config, Config
from ext import db

###此方法负责初始化app
def create_app(config_name):

    app=Flask(__name__,
            template_folder='templates', #指定模板路径，可以是相对路径，也可以是绝对路径。
            static_folder='dist',  #指定静态文件前缀，默认静态文件路径同前缀
            static_url_path='',     #指定静态文件存放路径。
             )
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # @app.before_request
    # def req_before():
    #     request.myvalues = MyRequest()

    ###初始化数据库
    db.init_app(app)

    ###初始化上传下载和导出目录
    init_static_path()

    ###注册蓝图
    register_app(app)
    ###初始化日志
    init_log()

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app


def init_static_path():
    """
    初始化上传下载所需目录
    :return:
    """
    ###初始化上传目录
    if not os.path.exists(Config.UPLOAD_PATH):
        os.makedirs(Config.UPLOAD_PATH)

    ###初始化导出excel目录
    if not os.path.exists(Config.EXPORT_PATH):
        os.makedirs(Config.EXPORT_PATH)

        ###初始化导入excel目录
    if not os.path.exists(Config.IMPORT_PATH):
        os.makedirs(Config.IMPORT_PATH)


