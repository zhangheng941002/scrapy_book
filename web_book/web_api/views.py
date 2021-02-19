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


@api_view(["GET"])
def book_type(request):
    data = request.data

    resp = BookTypeModel.objects.all()
    data = BookTypeModelSerializer(resp, many=True)
    return Response({"status": 1, "msg": "成功", "results": data.data})


@api_view(["GET"])
def book_type_info(request):
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
    query_params = request.query_params
    book_id = query_params.get("book")
    page = query_params.get("page", 1)
    page_size = page_size_limit(query_params.get("page_size", 100))
    limit, offset = get_page_limit(page_size, page)
    book_chapters = BookChapterModel.objects.filter(book_id=book_id).order_by("num")
    counts = book_chapters.count()
    resp = book_chapters[limit:offset]
    data = BookChapterSerializer(resp, many=True)
    return Response({"status": 1, "msg": "成功", "counts": counts,  "results": data.data})
