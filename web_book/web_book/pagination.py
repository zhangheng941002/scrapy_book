from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    # default_limit = 10             # 向后找几条的默认配置
    # limit_query_param = "limit"     # 请求参数中的limit参数名
    # offset_query_param = "offset"   # 请求参数中的offset参数名
    # max_limit = 100                   # 最大的寻找条数

    def paginate_queryset(self, queryset, request, view=None):
        return super(CustomPageNumberPagination, self).paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response({

            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'current': self.page.number,
            'results': data,
        })
