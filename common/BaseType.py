# -*- coding: utf-8 -*-
from common.Logger import Logger
class baseType:
    def __init__(self, filename: str = None):
        """[summary]
           初始化Logger物件
        Args:
            filename ([string], optional): 如果是繼承此物件，filename為NONE反之傳入檔名 Defaults to None.
        """
        if not filename:
            self.__log = Logger(
                './log/' + self.__class__.__name__ + '.log', level='debug')
        else:
            self.__log = Logger(
                './log/' + filename + '.log', level='debug')

    def writeLog(self, text: str):
        """[summary]
            Write Info
        Args:
            text ([string]): messages
        """
        self.__log.logger.info(text)

    def writeError(self, text: str):
        """[summary]
            Write Error
        Args:
            text ([string]): messages
        """
        self.__log.logger.error(text)

    def writeWarning(self, text: str):
        """[summary]
            Write Warning
        Args:
            text ([string]): messages
        """
        self.__log.logger.warning(text)

    def writeDebug(self, text: str):
        """[summary]
            Write Debug
        Args:
            text ([string]): messages
        """
        self.__log.logger.debug(text)

    def writeCritical(self, text: str):
        """[summary]
            Write Critical
        Args:
            text ([string]): messages
        """
        self.__log.logger.critical(text)
