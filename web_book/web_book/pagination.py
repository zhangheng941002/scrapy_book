from rest_framework.response import Response

from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):

        return super(CustomPageNumberPagination, self).paginate_queryset(queryset, request, view)
