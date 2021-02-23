# coding:utf-8

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .utils import get_page_limit, page_size_limit


class BookAllInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ServiceIpRelations
    """
    # queryset = BookAllInfoModel.objects.all()
    serializer_class = BookAllInfoModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = tuple([field.attname for field in BookAllInfoModel._meta.fields])

    def get_queryset(self):
        return BookAllInfoModel.objects.all()

    def list(self, request, *args, **kwargs):
        books = self.get_queryset().filter(status=0)
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 200)
        limit, offset = get_page_limit(page_size, page)
        book = books[limit:offset]
        data = BookAllInfoModelSerializer(book, many=True)
        return Response({"results": data.data})


@api_view(["POST"])
def search(request):
    """
    通过书名或者作者名查询书籍
    :param request:
        {
            "query_type":查询类型,  # 1/2(书名/作者名)
            "content": "content"
        }
    :return:
    """
    data = request.data
    query_type = data.get("query_type", 0)
    content = data.get("content", None)
    page = data.get("page", 1)
    page_size = page_size_limit(data.get("page_size", 20))
    limit, offset = get_page_limit(page_size, page)
    if not query_type or not content:
        return Response({"status": 0, "msg": "缺少必要参数"})
    if query_type == 1:
        # 书名模糊搜索
        query_data = {
            "book_name__contains": content
        }
    elif query_type == 2:
        # 作者名模糊搜索
        query_data = {
            "author_id__author_name__contains": content
        }
    else:
        return Response({"status": 0, "msg": "query_type超出范围"})

    books = BookModel.objects.filter(**query_data)
    counts = books.count()
    resp = books[limit:offset]
    data = BookModelSerializer(resp, many=True)
    return Response({"status": 1, "msg": "成功", "counts": counts, "results": data.data})


@api_view(["GET"])
def book_type(request):
    """
    分类列表
    :param request:
    :return:
    """

    resp = BookTypeModel.objects.all()
    data = BookTypeModelSerializer(resp, many=True)
    return Response({"status": 1, "msg": "成功", "results": data.data})


@api_view(["GET"])
def book_info(request):
    """
    通过分类查找书籍
    :param request:
    :return:
    """

    query_params = request.query_params
    type_id = query_params.get("type")
    page = query_params.get("page", 1)
    page_size = page_size_limit(query_params.get("page_size", 20))
    limit, offset = get_page_limit(page_size, page)
    books = BookModel.objects.filter(type_id=type_id)
    counts = books.count()
    resp = books[limit:offset]
    data = BookModelSerializer(resp, many=True)
    return Response({"status": 1, "msg": "成功", "counts": counts, "results": data.data})


@api_view(["GET"])
def book_chapter(request):
    """
    书的章节列表
    :param request:
    :return:
    """
    query_params = request.query_params
    book_id = query_params.get("book")
    page = query_params.get("page", 1)
    page_size = page_size_limit(query_params.get("page_size", 100))
    limit, offset = get_page_limit(page_size, page)
    book_chapters = BookChapterModel.objects.filter(book_id=book_id).order_by("num")
    counts = book_chapters.count()
    resp = book_chapters[limit:offset]
    data = BookChapterSerializer(resp, many=True)
    return Response({"status": 1, "msg": "成功", "counts": counts, "results": data.data})


@api_view(["GET"])
def chapter_content(request):
    """
    每一章的相信内容
    :param request:
    :return:
    """
    query_params = request.query_params
    book_id = query_params.get("book")
    chapter_num = query_params.get("chapter_num", 1)

    book_chapters = BookChapterModel.objects.filter(book_id=book_id, num=chapter_num)
    if not book_chapters.exists():
        return Response({"status": 0, "msg": "没有查到"})
    data = ChapterContentSerializer(book_chapters, many=True)
    return Response({"status": 1, "msg": "成功", "results": data.data})
