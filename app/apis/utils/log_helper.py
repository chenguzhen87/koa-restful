import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
import os

mylog = logging.getLogger()
def init_log():
    logpath = "/var/log"
    try:
        if not os.path.exists(logpath):
            os.makedirs(logpath)
    except:
        print("创建日志目录失败")
        exit(1)
    if len(mylog.handlers) == 0:  # 避免重复
        # 输出到屏幕
        streamHandler = StreamHandler()
        streamHandler.setLevel(logging.ERROR)
        mylog.addHandler(streamHandler)
        # 输出到日志文件
        filename = os.path.join(logpath, 'run.log')
        fileTimeHandler = TimedRotatingFileHandler(filename, when="W0", backupCount=30)
        fileTimeHandler.suffix = "%Y%m%d.log"  # 设置 切分后日志文件名的时间格式 默认 filename+"." + suffix 如果需要更改需要改logging 源码
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(module)s.%(funcName)s Line:%(lineno)d%(message)s')
        fileTimeHandler.setFormatter(fmt)
        mylog.addHandler(fileTimeHandler)
        mylog.setLevel(logging.ERROR)