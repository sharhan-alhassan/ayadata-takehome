from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(
        self,
        data,
        message="Data retrieved successfully",
        status_code=status.HTTP_200_OK,
    ):
        return Response(
            OrderedDict(
                [
                    ("message", message),
                    ("status", status_code),
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("data", data),
                ]
            )
        )
