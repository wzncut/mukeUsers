# -*- coding: utf-8 -*-
# 引入文件
from scrapy.exceptions import DropItem
import json
import codecs
from datetime import datetime,timedelta
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class MyPipeline(object):
    def __init__(self):

        self.conn = MySQLdb.connect(user='root', passwd='123456', db='test', host='localhost', charset="utf8",
                                    use_unicode=True)
        print ('-----------Mysql connect!-----------')
        self.cursor = self.conn.cursor()
        # 打开文件
        # self.file = open('data.json', 'w')

    #     self.file =codecs.open('data.json', 'w', encoding='utf-8')
    # #该方法用于处理数据
    # def process_item(self, item, spider):
    #     #读取item中的数据

    #     line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    #     #写入文件
    #     self.file.write(line)
    #     #返回item
    #     return item

    # pipeline默认调用
    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "insert into useritem(name, sex, privince, job, time) values(%s, %s, %s, %s, %s)",
                (item['name'], item['sex'], item['privince'], item['job'], item['time']))
            print ('-----------sql excute!----------')
            # self.cursor.execute(
            #     "insert into mooc(title, student,introduction,url) values(%s, %s, %s, %s)",
            #     (item['title'], item['student'], item['introduction'],
            #      item['url']))

            self.conn.commit()


        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item

    # 异常处理
    def _handle_error(self, failue, item, spider):
        log.err(failure)

    # 该方法在spider被开启时被调用。
    def open_spider(self, spider):
        pass

    # 该方法在spider被关闭时被调用。
    def close_spider(self, spider):
        pass