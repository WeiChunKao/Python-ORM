from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.exc import DatabaseError
from common.config import Config
from common.BaseType import baseType
from typing import Any, List
import sys


class ORM:
    __instance = None

    def __init__(self, *args, **kwargs):
        self.engine = create_engine(
            f'mysql+pymysql://{Config().dbUserName}:{Config().dbUserPassword}@{Config().dbHost}:{Config().dbPort}/{Config().dbDatabase}', echo=False)
        # 取得資料庫資料
        self.metadata = MetaData()
        # 設定資料庫連線
        self.sessionMaker = sessionmaker(bind=self.engine)
        # 建立連線
        self.session = self.sessionMaker()
        # 建立log物件
        self.logger = baseType(self.__class__.__name__)

    def getSessions(self):
        """[summary]
        ORM 連線
        Returns:
            [sessionmaker]: [description]
        """
        return self.session

    def getMetaData(self):
        """[summary]
        取得資料庫資料
        Returns:
            [MetaData]: 
        """
        return self.metadata

    def setMapper(self, className: Any, table: Table) -> None:
        """[summary]
        設定Class與資料庫對應
        Args:
            className (Any):class
            table (Table): Table
        """
        self.mapper = mapper(className, table)

    def close(self):
        """[summary]
        關閉連線
        """
        self.session.close()

    def insert(self, data: List[Any]) -> None:
        try:
            self.session.add_all(data)
        except DatabaseError as de:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{de}")
            self.session.rollback()
        except Exception as e:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{e}")
            self.session.rollback()
        finally:
            self.session.commit()

    def deleteOne(self, className: Any, filterString: String, **kwargs: dict) -> None:
        """[summary]
        刪除單筆資料
        Args:
            className (Any): class物件
            filterString (Any): where條件式
            kwargs (Any): where條件的值
        """
        try:
            row = self.session.query(className).filter(
                text(filterString)
            ).params(**kwargs).one()
            self.session.delete(row)
        except DatabaseError as de:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{de}")
            self.session.rollback()
        except Exception as e:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{e}")
            self.session.rollback()
        finally:
            self.session.commit()

    def deleteAll(self, className: Any, filterString: String, **kwargs: dict) -> None:
        """[summary]
        刪除多筆資料
        Args:
            className (Any): class物件
            filterString (Any): where條件式
            kwargs (Any): where條件的值
        """
        try:
            row = self.session.query(className).filter(
                text(filterString)
            ).params(**kwargs).delete(synchronize_session=False)
        except DatabaseError as de:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{de}")
            self.session.rollback()
            self.close()
        except Exception as e:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{e}")
            self.session.rollback()
            self.close()
        finally:
            self.session.commit()

    def updateOne(self, className: Any, filterString: String, updateData: dict, **kwargs: dict) -> None:
        """[summary]
        更新單筆資料
        Args:
            className (Any): class物件
            filterString (Any):  where條件式
            updateData (dict): 更新的資料
            kwargs (Any): where條件的值
        """
        try:
            row = self.session.query(className).filter(
                text(filterString)
            ).params(**kwargs).one()
            for k, v in updateData.items():
                setattr(row, k, v)
            self.session.add(row)
        except DatabaseError as de:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{de}")
            self.session.rollback()
        except Exception as e:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{e}")
            self.session.rollback()
        finally:
            self.session.commit()

    def updateAll(self, className: Any, filterString: Any, updateData: dict, **kwargs: dict) -> None:
        """[summary]
        更新多筆資料
        Args:
            className (Any): class物件
            filterString (Any): where條件式
            updateData (dict): 需要更新的欄位名稱及值
            kwargs:where條件式的值
        """
        try:
            updata: dict = {}
            for k, v in updateData.items():
                updata[className.__dict__.get(k, '')] = v
            self.session.query(className).filter(
                text(filterString).params(**kwargs)
            ).update(
                updata, synchronize_session=False)
        except DatabaseError as de:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{de}")
            self.session.rollback()
        except Exception as e:
            self.logger.writeError(
                f"{sys._getframe().f_code.co_name}=>{e}")
            self.session.rollback()
        finally:
            self.session.commit()
