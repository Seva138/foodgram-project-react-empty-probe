from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    """Custom pagination class, which redefines page_size_query_param method
    from 'page_size' to 'limit'.
    """
    page_size_query_param = 'limit'
