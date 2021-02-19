import scrapy
from iqiwx.items import IqiwxItem, BookInfoItem, PageItem, BookChapterItem
from iqiwx.utils import new_headers


class IqiwxSpider(scrapy.Spider):
    name = 'bookSpider'
    allowed_domains = ['iqiwx.com']
    start_urls = ['http://www.iqiwx.com']
    base_url = "http://www.iqiwx.com"
    end_url = ".html"

    def parse(self, response):

        type_list = response.xpath("//div[@class='nav']//li/a/h2/text()").extract()
        type_url_list = response.xpath("//div[@class='nav']//li/a/@href").extract()
        for type_name, type_url in zip(type_list, type_url_list):

            next_url = self.base_url + type_url
            flag = next_url.split("_")
            if len(flag) > 1:
                item = IqiwxItem()
                item["type_name"] = type_name
                item["type_url"] = next_url
                item["type_url_first"] = flag[0]
                yield scrapy.Request(next_url, callback=self.page_parse, meta={'item': item}, headers=new_headers())
        # base xpath
        # base = response.xpath("//div[@class='listlie']")
        # for each in base:
        #     # 每一个大的分类项
        #     type_name = each.xpath("./h2/text()").extract()
        #     # 图书总URL
        #     book_urls = each.xpath("./ul/li/a/@href").extract()
        #     # 书名
        #     book_names = each.xpath('./ul/li/a/text()').extract()
        #     # 作者
        #     book_authors = each.xpath('./ul/li/text()').extract()
        #     for book_url, book_name, book_author in zip(book_urls, book_names, book_authors):
        #         item = IqiwxItem()
        #         item['type_name'] = type_name
        #         item['book_url'] = book_url
        #
        #         item['book_name'] = book_name
        #         item['book_author'] = book_author.split("/")[1]
        #
        #         yield item
        # yield scrapy.Request(book_url, callback=self.second_parse, meta={'item': item})

    # 获取所有分类，所有页数信息
    def page_parse(self, response):
        item = response.meta['item']

        type_url_first = item["type_url_first"]
        type_name = item["type_name"]
        type_url = item["type_url"]
        # 分类中的页码提取
        page_data = response.xpath("//div[@class='pages']/div[@class='pagelink']/text()").extract()  # ['第 1/672 页 ']

        page_handle = page_data[0].split(" ")[1].split("/")  # ["1", "10"]
        for _page in range(1, int(page_handle[1]) + 1):
            next_url = "{type_url_first}_{page}{end_url}".format(type_url_first=type_url_first, page=str(_page),
                                                                 end_url=self.end_url)
            page_item = PageItem()
            page_item["page_url"] = next_url
            page_item["type_name"] = type_name
            page_item["type_url"] = type_url
            yield scrapy.Request(next_url, callback=self.book_first_parses, meta={'item': page_item},
                                 headers=new_headers())

    # 获取书的基本信息
    def book_first_parses(self, response):
        item = response.meta['item']
        type_name = item["type_name"]
        type_url = item["type_url"]
        # 进去每本书的url
        book_login_urls = response.xpath("//div[@id='sitebox']//dt/a/@href").extract()
        # 书的封面
        book_imgs = response.xpath("//div[@id='sitebox']//dt/a/img/@src").extract()
        # 书名
        book_names = response.xpath("//div[@id='sitebox']//dt/a/img/@alt").extract()
        # 作者+最新章节
        book_authors_and_chapters = response.xpath("//div[@id='sitebox']//dd[@class='book_other']//a/text()").extract()
        book_authors = []
        for i, book_authors_and_chapter in zip(range(0, len(book_authors_and_chapters)), book_authors_and_chapters):
            if i % 2 == 0:
                book_authors.append(book_authors_and_chapter)
        # 书的简介
        book_intros = response.xpath("//div[@id='sitebox']//dd[@class='book_des']/text()").extract()
        for book_login_url, book_img, book_name, book_author, book_intro in zip(book_login_urls, book_imgs, book_names,
                                                                                book_authors, book_intros):
            book_item = BookInfoItem()
            book_item["type_name"] = type_name
            book_item["type_url"] = type_url
            book_item["book_name"] = book_name
            book_item["book_author"] = book_author
            book_item["book_img"] = book_img
            book_item["book_login_url"] = book_login_url
            book_item["book_intro"] = book_intro

            # yield book_item
            yield scrapy.Request(book_login_url, callback=self.book_chapter_login_parses, meta={'item': book_item},
                                 headers=new_headers())

    # 进入每本书，获取进入所有章节的URL
    def book_chapter_login_parses(self, response):
        item = response.meta['item']
        # 所有章节进去的url,需要拼接
        chapter_url = response.xpath("//div[@class='newrap']/strong/a/@href").extract()
        for each_chapter_url in chapter_url:
            next_url = self.base_url + each_chapter_url
            item["chapter_login_url"] = next_url
            yield scrapy.Request(next_url, callback=self.book_chapter_parses, meta={'item': item},
                                 headers=new_headers())

    # 获取所有章节的URL
    def book_chapter_parses(self, response):
        item = response.meta['item']

        type_name = item["type_name"]
        type_url = item["type_url"]
        book_login_url = item["book_login_url"]
        book_name = item["book_name"]
        book_author = item["book_author"]
        book_img = item["book_img"]
        book_intro = item["book_intro"]
        chapter_login_url = item["chapter_login_url"]
        # yield item

        # 所有章节进去的url,需要拼接
        chapter_urls = response.xpath("//div[@id='readerlist']//li/a/@href").extract()
        # 章节名称
        chapter_names = response.xpath("//div[@id='readerlist']//li/a/text()").extract()
        for chapter_url, chapter_name, index in zip(chapter_urls, chapter_names, range(1, len(chapter_names)+1)):
            chapter_item = BookChapterItem()

            next_url = chapter_login_url + chapter_url
            chapter_item["book_name"] = book_name
            chapter_item["book_login_url"] = book_login_url
            chapter_item["type_name"] = type_name
            chapter_item["type_url"] = type_url
            chapter_item["book_author"] = book_author
            chapter_item["book_img"] = book_img
            chapter_item["book_intro"] = book_intro
            chapter_item["chapter_login_url"] = chapter_login_url
            chapter_item["chapter_name"] = chapter_name.replace(r"?", "")
            chapter_item["chapter_url"] = next_url
            chapter_item["num"] = index
            # yield chapter_item
            yield scrapy.Request(next_url, callback=self.finally_parses, meta={'item': chapter_item},
                                 headers=new_headers())

    # 每一章节的文本信息
    def finally_parses(self, response):
        item = response.meta['item']
        #
        chapter_content = response.xpath("//div[@id='content']/text()").extract()
        item["chapter_content"] = chapter_content
        yield item
