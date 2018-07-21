import uuid
from datetime import datetime
import socket
from functools import wraps
import time

def getMaxTime():
    return datetime.strptime("2100-01-01 01:01:01", "%Y-%m-%d %H:%M:%S")

def stringToDate(string):
    """
    #把字符串转成date
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d")

def stringToDatetime(string):
    """
    #把字符串转成datetime
    :param string:
    :return:
    """
    return datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

def dateToTime(timestring):
    """
    date转时间戳
    :param timestring:
    :return:
    """
    return time.mktime(time.strptime(timestring, '%Y-%m-%d'))

def datetimeToTime(timestring):
    """
    datetime转时间戳
    :param timestring:
    :return:
    """
    return time.mktime(time.strptime(timestring, '%Y-%m-%d %H:%M:%S'))

def getSysDateTime():
    """
    获取系统当前时间
    :return:
    """
    return time.time()

def getSysDateTimeStr():
    """
    获取系统当前时间
    :return:
    """
    strTime= time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    return strTime

#把时间戳转成字符串形式
def timeToDatetime(stamp):
    """
    时间戳转datetime
    :param stamp:
    :return:
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))

#####计算函数耗时装饰圈
def fun_time(func):
    @wraps(func)
    def wrapper(*args,**kargs):
        start_time=time.time()
        tempfun= func(*args,**kargs)
        end_time=time.time()
        real_time=end_time-start_time
        print("function name=%s,args=%s,kargs=%s real time is %s" %(func.__name__,args,kargs,real_time))
        return tempfun
    return wrapper

###获取本机IP
def get_ip():
    pcname = socket.getfqdn(socket.gethostname())
    pcip = socket.gethostbyname(pcname)
    return pcip

###搜索分割起始时间
def getStarttimeEndtimeBySearchDate(searchDate):
    startTime=stringToDate(searchDate.split(" - ")[0])
    endTime = stringToDate(searchDate.split(" - ")[1])
    return startTime,endTime

def getUuid():
    return str(uuid.uuid1())

