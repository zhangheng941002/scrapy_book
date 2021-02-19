# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
# useful for handling different item types with a single interface
from twisted.enterprise import adbapi


class MysqlTwistedPipeline(object):
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        param = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            port=settings["MYSQL_PORT"],
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        db_pool = adbapi.ConnectionPool("pymysql", **param)
        return cls(db_pool)

    def process_item(self, item, spider):

        # 使用twisted将mysql插入异步化
        query = self.db_pool.runInteraction(self.insert_data, item)

        # 处理异常
        query.addErrback(self.handle_error, spider)

        return item

    @staticmethod
    def handle_error(failure, spider):
        # 处理异步插入错误
        # 目前只打印了错误日志，可以将错误报出来，进行爬虫维护
        spider.logger.error(failure)

    @staticmethod
    def insert_data(cursor, item):
        """
        查询作者，分类，书本的原始信息是否存在，或许相应的数据id,进行章节内容的组装
        """

        insert_sql = """
            insert into book_all(book_name,book_login_url,type_name,type_url,book_author,book_img,book_intro,
            chapter_login_url, chapter_name, chapter_url, chapter_content, num)
            select %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s from DUAL where not exists(select id from book_all where book_name=%s and chapter_name=%s)
        """
        cursor.execute(insert_sql, (item["book_name"], item["book_login_url"], item["type_name"], item["type_url"],
                                    item["book_author"], item["book_img"], item["book_intro"],
                                    item["chapter_login_url"], item["chapter_name"],
                                    item["chapter_url"], str(item["chapter_content"]), item["num"], item["book_name"],
                                    item["chapter_name"]))

