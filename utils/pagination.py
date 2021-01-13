from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


# 重写PageNumberPagination类
class MyPagination(PageNumberPagination):
    # 指定默认每页显示数量
    page_size = 10
    # 指定第几页
    page_query_param = 'page'
    # 指定每页显示数量
    page_size_query_param = 'size'
    # 指定每页最大显示数量，如果前端指定的数量超出该数量，则显示最大值
    max_page_size = 50
    page_query_description = '第几页'
    page_size_query_description = '每页几条'

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data['current_page_num'] = self.page.number
        response.data['total_pages'] = self.page.paginator.num_pages
        return response
        # current_pages = self.page.number
        # total_pages = self.page.paginator.num_pages
        # return Response(OrderedDict([
        #     ('count', self.page.paginator.count),
        #     ('next', self.get_next_link()),
        #     ('previous', self.get_previous_link()),
        #     ('results', data),
        #     ('current_page_num', current_pages),
        #     ('total_pages', total_pages),
        # ]))