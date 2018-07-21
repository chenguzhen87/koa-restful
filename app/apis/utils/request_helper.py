import json

from flask import request, abort
from werkzeug.datastructures import MultiDict, CombinedMultiDict

from app.apis.utils.common import dateToTime, datetimeToTime


class MyRequest(object):
    '''
    简单封装request的的多个方法
    '''

    @classmethod
    def getAll(cls):
        args = []
        for d in request.args, request.form, request.json:
            if not isinstance(d, MultiDict):
                d = MultiDict(d)
            args.append(d)
        return CombinedMultiDict(args).to_dict()

    @classmethod
    def getList(cls, key, default=None,type=list):
        '''
        all parameter
        :param key: key
        :param d_value: None
        :return:
        '''
        if key in request.form:
            _value = request.form.getList(key)
        elif key in request.args:
            _value = request.args.getlist(key)
        else:
            abort(400, "Can't find parameter '" + key + "' in request.")
        try:
            return type(_value)
        except ValueError:
            if default is not None:
                return default
            else:
                abort(400, "The argument '" + key + "' must be " + type.__name__ + ".")

    def __getValue(self, key):
        """
        根据key获取value
        :param key:
        :return:
        """
        if key in request.form:
            _value = request.form.get(key)
        elif key in request.args:
            _value = request.args.get(key)
        elif request.json and key in request.json:
            _value = request.json.get(key)
        else:
            abort(400, "Can't find parameter '" + key + "' in request.")
        return _value

    @classmethod
    def get(cls, key, default=None, type=None):
        """
        获取value，默认不验证
        :param key:
        :param default:
        :param type:
        :return:
        """
        _value=cls.__getValue(cls,key)
        if type is not None and _value is not None:
            try:
                return type(_value)
            except ValueError:
                if default is not None:
                    return default
                else:
                    abort(400, "The argument '" + key + "' must be " + type.__name__ + ".")
        elif default is not  None:
            return default
        else:
            return _value

    @classmethod
    def get_verify_int(cls, key, default=None):
        """
        获取value，默认不验证
        :param key:
        :param default:
        :param type:
        :return:
        """
        _value = cls.__getValue(cls, key)
        if _value is not None:
            try:
                return int(_value)
            except ValueError:
                if default is not None:
                    return default
                else:
                    abort(400, "The argument '" + key + "' must be int.")
        elif default is not None:
            return default
        else:
            abort(400, "The argument '" + key + "' can not be empty.")

    @classmethod
    def get_verify_float(cls, key, default=None):
        """
        获取value，默认不验证
        :param key:
        :param default:
        :param type:
        :return:
        """
        _value = cls.__getValue(cls, key)
        if _value is not None:
            try:
                return float(_value)
            except ValueError:
                if default is not None:
                    return default
                else:
                    abort(400, "The argument '" + key + "' must be int.")
        elif default is not None:
            return default
        else:
            abort(400, "The argument '" + key + "' can not be empty.")

    @classmethod
    def get_verify_dict(cls, key, default=None):
        '''
        all parameter
        :param key: key
        :param d_value: None
        :return:
        '''
        _value = cls.__getValue(cls, key)
        if _value is not None:
            try:
                return eval(_value)
            except:
                if default is not None:
                    return default
                else:
                    abort(400, "The argument '" + key + "' must be list.")
        elif default is not None:
            return default
        else:
            abort(400, "The argument '" + key + "' can not be empty.")

    @classmethod
    def get_verify_list(cls, key, default=None):
        '''
        all parameter
        :param key: key
        :param d_value: None
        :return:
        '''
        _value = cls.__getValue(cls, key)
        if _value is not None:
            try:
                return json.loads(_value)
            except:
                if default is not None:
                    return default
                else:
                    abort(400, "The argument '" + key + "' must be list.")
        elif default is not None:
            return default
        else:
            abort(400, "The argument '" + key + "' can not be empty.")

    @classmethod
    def get_verify_date(cls, key, default=None):
        """
        验证日期字段
        :param key:
        :param default:
        :return:
        """
        _value=cls.__getValue(cls,key)
        if _value is not None:
            try:
                return dateToTime(_value)
            except:
                if default is not None:
                    return default
                else:
                    abort(400, "The argument '" + key + "' must be date like XXXX-XX-XX.")
        elif default is not None:
            return default
        else:
            abort(400, "The argument '" + key + "' can not be empty.")

    @classmethod
    def get_verify_datetime(cls, key, default=None):
        """
        验证日期字段
        :param key:
        :param default:
        :return:
        """
        _value=cls.__getValue(cls,key)
        if _value is not None:
            try:
                return datetimeToTime(_value)
            except:
                if default is not None:
                    return default
                else:
                    abort(400, "The argument '" + key + "' must be datetime like XXXX-XX-XX XX:XX:XX.")
        elif default is not None:
            return default
        else:
            abort(400, "The argument '" + key + "' can not be empty.")

    @classmethod
    def get_verify_bool(cls, key, default=None):
        """
        验证bool值
        :param key:
        :param default:
        :return:
        """
        _value=cls.__getValue(cls,key)
        if _value is not None:
            if _value=="true" or _value=="True" or _value=="1":
                return True
            elif _value=="false" or _value=="False" or _value=="0":
                return False
            elif default is not None:
                return default
            else:
                abort(400, "The argument '" + key + "' must be " + type.__name__ + ".")
        elif default is not None:
            return default
        else:
            abort(400, "The argument '" + key + "' can not be empty.")

    @classmethod
    def get_verify_empty(cls, key, default=None,errmsg=""):
        """
        验证字符串非空
        :param key:
        :param default:
        :param type:
        :param errmsg:
        :return:
        """
        _value=cls.get(key,default,str)
        ###验证字符串非空None or '  '
        if not _value or not _value.strip():
            if not errmsg:
                abort(400,"The argument '" + key + "' can't be empty.")
            abort(400,errmsg)
        return _value