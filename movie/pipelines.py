# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class MoviePipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            db=settings['MYSQL_DBNAME'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 异步插入
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)
        import codecs
        fw = codecs.open('errLog.txt', 'a', 'utf-8')
        fw.write("网站地址：" + item['url'] + "\r\n" + str(failure))
        fw.close()

    def KeyJudge(self, item_dict, value):
        if value in item_dict.keys():
            return item_dict[value]
        else:
            return None

    def do_insert(self,cursor,item):
        channel = self.KeyJudge(item,"channel")

        insert_sql = """
                        insert into movie(
                        title,
                        thumb,
                        url,
                        duration,
                        post_date,
                        video_url,
                        views_num,
                        channel)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql, (
            item['title'],
            item['thumb'],
            item['url'],
            item['duration'],
            item['post_date'],
            item['video_url'],
            item['views_num'],
            channel
        ))