# coding:utf-8
import re
import cn2an
import requests
from django_redis import get_redis_connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.transaction import atomic

from web_api.models import *
from .models import *


@api_view(["GET"])
def handle_book_all_info(request):
    data = request.data
    http_host = request.META.get("HTTP_HOST")
    http_type = request.META.get("wsgi.url_scheme")
    redis = get_redis_connection("redis")
    is_finish = int(redis.get("is_finish"))
    if is_finish:
        return Response({"status": 1, "msg": "处理完毕", "result": {}})
    # page = redis.get("page")
    url = "{}://{}{}".format(http_type, http_host, "/web/book?page=1")
    resp = requests.get(url).json()

    results = resp.get("results")
    if not results:
        redis.set("is_finish", 1)
    ids = []
    with atomic():
        for each in results:
            id = each.get("id")
            book_name = each.get("book_name")
            type_name = each.get("type_name")
            book_author = each.get("book_author")
            book_img = each.get("book_img")
            book_intro = each.get("book_intro")
            chapter_name = each.get("chapter_name")
            chapter_content = each.get("chapter_content")
            num = each.get("num")

            book_types = BookTypeModel.objects.filter(type_name=type_name)
            if not book_types.exists():
                book_type = BookTypeModel.objects.create(type_name=type_name, status=1)
            else:
                book_type = book_types.first()

            authors = AuthorModel.objects.filter(author_name=book_author)
            if not authors.exists():
                author = AuthorModel.objects.create(author_name=book_author)
            else:
                author = authors.first()

            books = BookCreateModel.objects.filter(book_name=book_name, type_id=book_type.id, author_id=author.id)
            if not books.exists():
                book = BookCreateModel.objects.create(book_name=book_name, img=book_img, author_id=author.id,
                                                type_id=book_type.id,
                                                book_intro=book_intro)
            else:
                book = books.first()

            chapters = BookChapterCreateModel.objects.filter(book_id=book.id, chapter_name=chapter_name)
            if not chapters.exists():

                _chapter_content = chapter_content.replace("\\xa0\\xa0\\xa0\\xa0", "<br /><br />&nbsp;&nbsp;&nbsp;&nbsp;").replace("'", "").replace(",", "").replace("[", "").replace("]", "")

                BookChapterCreateModel.objects.get_or_create(book_id=book.id, chapter_name=chapter_name,
                                                       chapter_content=_chapter_content, num=num)

            ids.append(id)

        if ids:
            BookAllInfoModel.objects.filter(id__in=ids).update(status=1)
    return Response({"status": 1, "msg": "成功", "result": results})
