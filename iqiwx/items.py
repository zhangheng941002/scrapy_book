# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IqiwxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 分类项
    type_name = scrapy.Field()
    # 分类url
    type_url = scrapy.Field()
    type_url_first = scrapy.Field()


class PageItem(IqiwxItem):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 分页
    page_url = scrapy.Field()


class BookInfoItem(IqiwxItem):
    # 图书总URL
    book_login_url = scrapy.Field()
    # 书名
    book_name = scrapy.Field()
    # 作者
    book_author = scrapy.Field()

    # 图书背景图
    book_img = scrapy.Field()
    # 书的简介
    book_intro = scrapy.Field()
    # 进入每本书所有章节的URL
    chapter_login_url = scrapy.Field()


class BookChapterItem(BookInfoItem):
    # 章节的URL
    chapter_url = scrapy.Field()
    # 章节名称
    chapter_name = scrapy.Field()
    # 章节内容
    chapter_content = scrapy.Field()
