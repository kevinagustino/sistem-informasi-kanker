from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    """
    Custom pagination untuk API:
    - page_size: jumlah item per halaman
    - page_size_query_param: parameter untuk mengubah jumlah item per halaman
    - max_page_size: jumlah maksimum item yang bisa diminta
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100