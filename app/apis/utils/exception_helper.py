"""
自定义异常处理
"""

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class MyError(Error):
    """
    抛出一个常规错误
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class InputError(Error):
    """抛出一个输入错误

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class ExcelError(Error):
    """
    抛出一个Excel读取/写入错误
    """
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message