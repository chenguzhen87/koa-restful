from flask import Blueprint
from app.apis.utils.response_helper import MyResponse

#在蓝本中编写错误处理程序稍有不同，如果使用 errorhandler 修饰器，那么只有蓝本中的错误才
#能触发处理程序。要想注册程序全局的错误处理程序，必须使用 app_errorhandler。
#处理404错误

error = Blueprint('error',__name__)


@error.app_errorhandler(400)
def not_found(error):
    """
    Bad Request
    如果浏览器发送一些东西给应用，应用或服务器无法处理，则抛出,可用于参数校验
    :param error:
    :return:
    """
    myRes = MyResponse()
    myRes.msg = error.description
    myRes.code = 400
    return myRes.to_json()

@error.app_errorhandler(401)
def not_found(error):
    """
    Unauthorized
    如果用户没有认证则抛出
    :param error:
    :return:
    """
    myRes = MyResponse()
    myRes.msg = error.description
    myRes.code = 401
    return myRes.to_json()

@error.app_errorhandler(403)
def not_found(error):
    """
    Forbidden
    如果用户没有权限请求该资源但是已经认证过了，则抛出。
    :param error:
    :return:
    """
    myRes = MyResponse()
    myRes.msg = error.description
    myRes.code = 403
    return myRes.to_json()

@error.app_errorhandler(404)
def not_found(error):
    """
    URL Not Found
    如果资源不存在并且从来没存在过则抛出。
    :param error:
    :return:
    """
    ###传统方式
    myRes = MyResponse()
    myRes.msg = error.description
    myRes.code=404
    return myRes.to_json()


@error.app_errorhandler(405)
def not_found(error):
    """
    Method Not Allowed
    如果服务器使用一个资源无法处理的方法，则抛出。
    :param error:
    :return:
    """
    myRes=MyResponse()
    myRes.msg=error.description
    myRes.code=405
    return myRes.to_json()

@error.app_errorhandler(500)
def internal_server_error(error):
    """
    Internal Server Error
    如果一个内部服务错误发生则抛出。如果在调度时一个未知错误发生，这是一个很好的后备东西。
    :param error:
    :return:
    """
    myRes = MyResponse()
    myRes.msg = error.description
    myRes.code = 500
    return myRes.to_json()