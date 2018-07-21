import json
from datetime import datetime
import math
import decimal
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app.apis.utils.common import getMaxTime, timeToDatetime
from app.apis.utils.exception_helper import MyError
from ext import db_session


class MySqlalchemy(object):
    """
    sqlalchemy帮助类
    """
    ###构造方法
    def __init__(self):
        pass

    @classmethod
    def comAdd(cls,model):
        """
        添加方法
        :param model:
        :return:
        """
        try:
            db_session.add(model)
            db_session.commit()
        except SQLAlchemyError as ex:
            raise ex
        finally:
            db_session.close()

    @classmethod
    def comDel(cls,model,filters):
        """
        删除方法
        :param model:
        :param filters:
        :return:
        """
        try:
            rows=db_session.query(model).filter(*filters).delete(synchronize_session=False)
            db_session.commit()
            if rows<1:
                raise SQLAlchemyError("操作失败")
        except SQLAlchemyError as ex:
            raise ex
        finally:
            db_session.close()

    @classmethod
    def comUpdate(cls, model,filters, attrs):
        """
        修改方法
        :param model:
        :param filters:
        :param attrs:
        :return:
        """
        try:
            rows=db_session.query(model).filter(*filters).update(attrs)
            db_session.commit()
            if rows<1:
                raise SQLAlchemyError("操作失败")
        except SQLAlchemyError as ex:
            raise ex
        finally:
            db_session.close()

    @classmethod
    def comAdds(cls,models):
        """
        批量添加
        :param models:
        :return:
        """
        try:
            if isinstance(models,(list,tuple)):
                db_session.begin_nested()
                for model in models:
                    db_session.add(model)
                db_session.commit()
            else:
                raise MyError("Models mast be list or tuple.")
        except SQLAlchemyError as ex:
            db_session.rollback()
            raise ex
        finally:
            db_session.close()

    @classmethod
    def comDels(cls, models, ids):
        """
        批量删除
        :param models:
        :param ids:
        :return:
        """
        try:
            if isinstance(models, (list, tuple)) and isinstance(ids, (list, tuple)):
                db_session.begin_nested()
                for model in models:
                    rows=db_session.query(models).filter(model.Fid == id).delete(synchronize_session=False)
                    if rows < 1:
                        raise SQLAlchemyError("操作失败")
                db_session.commit()
            else:
                raise MyError("Models and ids mast be list or tuple.")
        except SQLAlchemyError as ex:
            db_session.rollback()
            raise ex
        finally:
            db_session.close()

    @classmethod
    def comUpdates(cls, list_model, id, attrs):
        """
        批量修改
        :param list_model:
        :param id:
        :param attrs:
        :return:
        """
        try:
            db_session.begin_nested()
            for model in list_model:
                rows=db_session.query(model).filter(model.Fid == id).update(attrs)
                if rows < 1:
                    raise SQLAlchemyError("操作失败")
            db_session.commit()
        except SQLAlchemyError as ex:
            db_session.rollback()
            raise ex
        finally:
            db_session.close()

    @classmethod
    def convertToList(cls,query_datas):
        """
        将sqlalchemy的query对象转换为list对象
        :param query_datas:
        :return:list
        """
        fields = []
        for obj in query_datas:
            temp_dict=cls.convertToDict(obj)
            fields.append(temp_dict)
        return fields

    @classmethod
    def convertToDict(cls,query_data):
        """
        将sqlalchemy的query对象转换为dict对象
        :param query_data:
        :return:dict
        """
        temp_dict={}
        for field in dir(query_data):
            if not field.startswith('_') and field != 'metadata' and field != 'query' and field!='query_class':
                data = query_data.__getattribute__(field)
                try:
                    if (field=="TIME_CREATE" or field=="TIME_MODIFY") and isinstance(data, decimal.Decimal):
                        data = timeToDatetime(data)
                    elif isinstance(data, datetime):
                        if data==getMaxTime():
                            data=""
                        else:
                            data = data.strftime('%Y-%m-%d %H:%M:%S')
                    elif isinstance(data, list):
                        data=cls.convertToList(data)
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    temp_dict[field] = data
                except TypeError as ex:
                    temp_dict[field] = None
        return temp_dict


    def __convertToPageDict(self,query_datas, currentPage, pageSize, total):
        """
        将sqlalchemy的query对象转换为page dict对象
        :param query_datas:
        :return:dict
        """
        data = {}
        data["data"] = self.convertToList(query_datas)
        data["currentPage"] = currentPage
        data["pageSize"] = pageSize
        if total == 0:
            data["pageCount"] = 1
        else:
            data["pageCount"] = math.ceil(total / pageSize)
        data["total"] = total
        return data

    def __getRealQuery(self,columns,outerjoins=[], filters=None,orders=None):
        """
        私有方法，通用查询方法
        :param columns:
        :param outerjoins:
        :param filters:
        :param orders:
        :return:
        """
        if columns is not None:
            if isinstance(columns, (tuple, list)):
                query = db_session.query(*columns)
            else:
                query = db_session.query(columns)
        if outerjoins is not None:
            if isinstance(outerjoins, (tuple, list)):
                query = query.outerjoin(*outerjoins)
            else:
                query = query.outerjoin(outerjoins)
        if filters is not None:
            if isinstance(filters, (tuple, list)):
                query = query.filter(*filters)
            else:
                query = query.filter(filters)
        if orders is not None:
            if isinstance(orders, (tuple, list)):
                query = query.order_by(*orders)
            else:
                query = query.order_by(orders)
        return query

    @classmethod
    def get_page_list(cls,currentPage,pageSize,pk,columns,outerjoins=[], filters=None,orders=None):
        """
        分页查询
        :param currentPage:
        :param pageSize:
        :param pk:
        :param columns:
        :param outerjoins:
        :param filters:
        :param orders:
        :return:
        """
        query=cls.__getRealQuery(cls,columns,outerjoins,filters,orders)
        query_total = cls.__getRealQuery(cls,func.count(pk), outerjoins, filters, orders)
        ###查询
        start_index = (currentPage - 1) * pageSize
        total=query_total.scalar()
        query_data=query.limit(pageSize).offset(start_index).all()
        return cls.__convertToPageDict(cls,query_data,currentPage,pageSize,total)

    @classmethod
    def get_all(cls, columns,outerjoins=None, filters=None,  orders=None):
        """
        查询所有
        :param columns:
        :param outerjoins:
        :param filters:
        :param orders:
        :return:
        """
        query = cls.__getRealQuery(cls, columns, outerjoins, filters, orders)
        query_data = query.all()
        return cls.convertToList(query_data)

    @classmethod
    def get_detail(cls, columns, outerjoins=None, filters=None):
        """
        单行查询
        :param columns:
        :param outerjoins:
        :param filters:
        :return:
        """
        query = cls.__getRealQuery(cls, columns, outerjoins, filters, None)
        query_data = query.one()
        return cls.convertToDict(query_data)

    @classmethod
    def get_detail_first(cls, columns, outerjoins=None, filters=None):
        query = cls.__getRealQuery(cls, columns, outerjoins, filters, None)
        query_data = query.first()
        return cls.convertToDict(query_data)