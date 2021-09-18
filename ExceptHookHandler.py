__author__ = "hwy"
import logging
import sys,os
import datetime

class ExceptHookHandler(object):
    def __init__(self):
        self.__LogFile =os.path.dirname(__file__) +"/log/runlog.log"
        self.__Logger = self.__BuildLogger()
        # 重定向异常捕获
        sys.excepthook = self.__HandleException

    # 创建logger类
    def __BuildLogger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)#设置log登记开关CRITICAL > ERROR > WARNING > INFO > DEBUG
        #formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        logger.addHandler(logging.FileHandler(self.__LogFile,mode="w+"))
        return logger

    def __HandleException(self, excType, excValue, tb):
        """
        :param excType:  异常类型
        :param excValue: 异常对象
        :param tb: 异常的trace back
        :return:
        """
        try:
            currentTime = datetime.datetime.now()
            self.__Logger.info('Timestamp: %s' % (currentTime.strftime("%Y-%m-%d %H:%M:%S")))
            self.__Logger.error("Uncaught exception：", exc_info=(excType, excValue, tb))
            self.__Logger.info('\n')
        except:
            pass
        # then call the default handler
        sys.__excepthook__(excType, excValue, tb)

