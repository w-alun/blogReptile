import pymysql
import threading


class DBUtil:
    def __init__(self):
        self.__db = pymysql.connect("localhost","root","root","db_python_reptile" )
        self.__cursor = self.__db.cursor()
        self.__semaphore=threading.Semaphore(1)

    def insertTbUrl(self,url):
        sql="insert into tb_url(url) values('%s')"%(url)
        try:
            self.__semaphore.acquire()
            self.__cursor.execute(sql)
            self.__db.commit()
        except Exception as e:
            # print(e)
            pass
        finally:
            self.__semaphore.release()
        pass

    def getTbUrl(self):
        sql="select * from tb_url"
        try:
            self.__semaphore.acquire()
            self.__cursor.execute(sql)
            result=self.__cursor.fetchall()
        finally:
            self.__semaphore.release()
        pass


    def get1000Url(self,index):
        sql = "select url from tb_url limit %d,100" % (index)
        try:
            self.__semaphore.acquire()
            result=self.__cursor.execute(sql)
        finally:
            self.__semaphore.release()
        pass

    def insertTbContent(self,content):
        sql="insert into tb_content(content) values(%s)"%(content)
        try:
            self.__semaphore.acquire()
            self.__cursor.execute(sql)
            self.__db.commit()
        finally:
            self.__semaphore.release()
        pass

    def getTbContent(self):
        sql="select * from tb_content"
        try:
            self.__semaphore.acquire()
            self.__cursor.execute(sql)
            result=self.__cursor.fetchall()
        finally:
            self.__semaphore.release()

    def getTb100Content(self,index):
        sql="select content from tb_content limit %d,100"%(index)
        try:
            self.__semaphore.acquire()
            self.__cursor.execute(sql)
            result = self.__cursor.fetchall()
        finally:
            self.__semaphore.release()
        pass


if __name__=="__main__":
    dbUtil=DBUtil()
    dbUtil.insertTbUrl("1")
