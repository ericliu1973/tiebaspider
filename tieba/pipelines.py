# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymysql.cursors
from twisted.enterprise import adbapi

class Beihuapipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlTwistedPiple(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
        self.table_name = 'your_table'
        query = self.dbpool.runInteraction(self.create_table)

    def create_table(self, cursor):
        sql = ''' CREATE TABLE IF NOT EXISTS `{tbname}` (
          `url` varchar(255) NOT NULL,
          `title` varchar(255) NOT NULL,
          `author_name` varchar(150) DEFAULT NULL,
          `content` longtext,
          `comments_num` varchar(20) DEFAULT NULL,
          `created_time` datetime DEFAULT NULL,
          `crawl_time` datetime NOT NULL,
          PRIMARY KEY (`url`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;

        '''
        try:
            cursor.execute(
                sql.format(tbname=self.table_name, create_time='create_time', mobile_phone='mobile_phone',
                           content='content',
                           crawl_time='crawl_time'))
        except Exception as e:
            print('创建表格失败，原因', e)


    @classmethod
    def from_settings(cls,settings):
        #传入settings参数
        dbparms = dict(
            host = settings["MYSQL_HOST"],
            db = settings["MYSQL_DBNAME"],
            user = settings["MYSQL_USER"],
            passwd = settings["MYSQL_PASSWORD"],
            port = settings["MYSQL_PORT"],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
        return item

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)


    def do_insert(self, cursor, item):
        try:
            insert_sql,params = item.get_insert_sql()
        except Exception as e:
            print("插入失败，原因:",e)
        else:
            cursor.execute(insert_sql,params)
            print('成功插入一条数据！')

