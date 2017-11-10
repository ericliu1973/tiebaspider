# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose
import re
from datetime import datetime

def change_date(_values):
    time = datetime.strptime(_values,'%Y-%m-%d %H:%M')
    return time

def change_blank(_values):
    #去掉content中的空格
    return _values.strip().encode('utf-8')

def change_int(_values):
    #转换为int型
    match_re = re.match(".*?(\d+).*",_values)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums

class BeihuaItemLoader(ItemLoader):
    #自定义itemloader
    default_output_processor = TakeFirst()

class BeihuaItem(scrapy.Item):
    title = Field(
        input_processor = MapCompose(change_blank)
    )
    url = Field()
    author_name = Field()
    content = Field(
        input_processor = MapCompose(change_blank)
    )
    created_time = Field(
        input_processor = MapCompose(change_date)
    )
    comments_num = Field(
        input_processor = MapCompose(change_int)
    )
    crawl_time = Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO your_name(url,title,author_name,content,comments_num,
                              created_time,crawl_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE comments_num=VALUES(comments_num)
                """
        params = (
                    self["url"],self["title"],self["author_name"],self["content"],self["comments_num"],
                    self["created_time"],self["crawl_time"]
                )
        return insert_sql,params
