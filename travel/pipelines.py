# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql


class TravelPipeline(object):
    def __init__(self):
        self.f = open("travel.json", "w", encoding='utf-8')

    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False, indent=4)
        self.f.write(content + '\n')
        return item

    def close_spider(self, spider):
        self.f.close()


class writeMysql(object):
    def __init__(self):
        self.client = pymysql.connect(
            host='47.112.212.177',
            port=3306,
            user='rdcBackers',  # 使用自己的用户名
            passwd='rdc123',  # 使用自己的密码
            db='rdc_travel_talking',  # 数据库名
            charset='utf8'
        )
        # self.client = pymysql.connect(
        #     host='localhost',
        #     port=3306,
        #     user='root',  # 使用自己的用户名
        #     passwd='2019',  # 使用自己的密码
        #     db='spiders',  # 数据库名
        #     charset='utf8'
        # )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        print(type(item['id']))
        sql = "insert into big_data_path(id,preview,title,introduction,content) " \
              "VALUES (%s,%s,%s,%s,%s)"
        # sql = 'insert into game(preview,title,introduction,content,comment_num,star_num,collection_num) ' \
              # 'VALUES (%s,%s,%s,%s,%d,%d,%d)'
        sqlExit = "SELECT title FROM big_data_path  WHERE title = ' %s '" % (item['title'])
        res = self.cur.execute(sqlExit)
        if res:
            return
        lis = (item['id'],
               item['preview'],
               item['title'],
               item['introduction'],
               item['content'])
               # item['comment_num'],
               # item['star_num'],
               # item['collection_num'])
        self.cur.execute(sql, lis)
        self.client.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.client.close()

