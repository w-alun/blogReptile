import requests
from bs4 import BeautifulSoup
import re
from DBUtil import DBUtil
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os, time, random


class BlogRepyilt:
    def __init__(self, urls):
        self.__rootPath = "https://www.cnblogs.com"
        self.__allUrl = set()  # 已经访问过的URL
        self.__resultUrl = set()  # 结果集
        self.__newUrl = set(urls)  # 新添加的URL
        self.__dbUtil = DBUtil()
        self.__resultL = 0
        pass

    def getUrl(self):
        urls = self.__newUrl.copy()  # 拷贝一份，一边遍历一边删除
        try:
            for url in urls:
                self.__allUrl.add(url)  # 已经访问了
                self.__newUrl.remove(url)  # 删除已经访问过的
                html = None
                try:
                    html = requests.get(url)
                except Exception as e:
                    print(e)
                    continue
                bs = BeautifulSoup(html.text, features="html.parser")
                hrefs = bs.find_all("a")
                for href in hrefs:
                    href = href.get("href")
                    if href != None and href != "" and href[0] == "/":
                        url = self.__rootPath + str(href)
                    else:
                        url = href

                    if href != None and self.__allUrl.__contains__(url) == False:  # 是否已经访问
                        if url.find("cnblogs") > 0:  # 是否是符合规则的URL
                            self.__newUrl.add(url)  # 符合规则添加到新的URL中
                        else:
                            self.__allUrl.add(url)  # 不符合规则直接扔掉
                        if self.__resultUrl.__contains__(url) == False and re.match(
                                "https://www\.cnblogs\.com/.*\d{7,8}\.html.*", url) is not None:
                            self.__resultUrl.add(url)
                            self.__dbUtil.insertTbUrl(url)
                            self.__resultL += 1
                            print("目前url条数：" + str(self.__resultL))
        except Exception as e:
            print(e)
        self.getUrl()
        pass


if __name__ == "__main__":
    blogRepyilt = BlogRepyilt({"https://www.cnblogs.com/jiaoxiangjie/p/6748039.html"})
    blogRepyilt.getUrl()

# s=""
# print(re.match("\w{5}.{3}\w{3}.\w{7}.\w{3}\/\w{1,10}\/.\/\d.\w{4}",s).group())
# print(re.match("https://www\.cnblogs\.com/.*\d{7,8}\.html.*",s))
# f = open('test.txt')
# s=f.readline()
# while s:
#     if re.match("https://www\.cnblogs\.com/.*\d{7,8}\.html.*",s) is not  None:
#         print(re.match("https://www\.cnblogs\.com/.*\d{7,8}\.html.*",s).group())
#     s=f.readline()


# def task():
#     t.getUrl()
#
# t = BlogRepyilt()
# if __name__ == '__main__':
#     executor = ProcessPoolExecutor(max_workers=11)
#     for i in range(11):
#         executor.submit(task, )
#     executor.shutdown(True)
