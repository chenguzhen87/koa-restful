import datetime
import os
import xlrd
import xlsxwriter
from xlrd import XLRDError

from app.apis.utils.exception_helper import ExcelError
from config import Config


class XlrdReader(object):
    """
    读取excel，适用于.xls and .xlsx
    """
    def __init__(self,file):
        self.file=file
        self.titles=[]
        self.datas=[]

    def readSheetToList(self,sh_number=None):
        """
        读取sheet转换为list
        :param sh_number:
        :return:
        """
        # 打开文件
        try:
            workbook = xlrd.open_workbook(self.file)
            # 打开工作表
            if sh_number:
                worksheet = workbook.get_sheet(sh_number)
            else:
                worksheet = workbook.sheets()[0]
            # 获得所有行数
            nrows = worksheet.nrows
            for x in range(nrows):
                if x ==0:
                    self.titles=worksheet.row_values(x)
                else:
                    self.datas.append(worksheet.row_values(x))
        except XLRDError as ex:
            raise ExcelError(ex)


    def readAllToDict(self):
        """
        读取所有的sheet转换为dict
        :return:
        """
        try:
            # 打开文件
            workbook = xlrd.open_workbook(self.file)
            # 打开工作表
            worksheets = workbook.sheets()
            dict_sheet={}
            for worksheet in worksheets:
                # 获得所有行数
                nrows = worksheet.nrows
                list_data = []
                for x in range(nrows):
                    list_data.append(worksheet.row_values(x))
                    dict_sheet[worksheet.name]=list_data
            return dict_sheet
        except XLRDError as ex:
            raise ExcelError(ex)



class XlsxwriterWriter(object):
    """
    写入到excel，只适用于xlsx
    """
    def __init__(self):
        self.filepath=Config.EXPORT_PATH
        self.filename=datetime.datetime.now().strftime('%Y%m%d%H%M%S')+".xlsx"
        self.file=os.path.join(self.filepath,self.filename)
        self.workbook = None

    def open(self):
        self.workbook = xlsxwriter.Workbook(self.file)

    def close(self):
        if self.workbook:
            self.workbook.close()

    def writeSheetbyList(self,df,titles=None,sheetname=None):
        """
        写入list到xlsx
        :param datas:
        :param sheetname:
        :return:
        """
        try:
            if sheetname:
                worksheet = self.workbook.add_worksheet(sheetname)
            else:
                worksheet = self.workbook.add_worksheet()
            # add_format() 为当前workbook添加一个样式名为titleformat
            titleformat = self.workbook.add_format()
            titleformat.set_bold(bold=True)  # 设置粗体字
            titleformat.set_font_size(11)  # 设置字体大小为11
            titleformat.set_font_name('Microsoft yahei')  # 设置字体样式为雅黑
            titleformat.set_align('left')  # 设置水平居中对齐
            titleformat.set_align('vcenter')  # 设置垂直居中对齐
            if titles is None:
                titles=df.columns
            for index_col, value in enumerate(titles):
                worksheet.write(0, index_col, value, titleformat)
            # 再添加一个样式rowformat,将作为数据行的格式
            rowformat = self.workbook.add_format()
            rowformat.set_bold(bold=False)
            rowformat.set_font_size(10)
            rowformat.set_font_name('Microsoft yahei')
            rowformat.set_align('left')
            rowformat.set_align('vcenter')
            rowformat.set_text_wrap()  # 设置自动换行
            column_len=len(titles)
            worksheet.set_column(0, 1, 20)
            worksheet.set_column(1,column_len-1,12)
            worksheet.set_column(column_len-1, column_len, 35)
            for index_row, row in enumerate(df.values):
                # 文本对齐方式
                for index_col, value in enumerate(row):
                    worksheet.write(index_row+1, index_col, value, rowformat)
        except ValueError as ex:
            raise ExcelError(ex)



