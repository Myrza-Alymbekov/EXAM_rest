from rest_framework.pagination import PageNumberPagination


class PostPagePagination(PageNumberPagination):
    page_size = 3
