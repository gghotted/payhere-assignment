from rest_framework.pagination import PageNumberPagination


def pagination_factory(**kwargs):
    return type(
        'PageNumberPagination',
        (PageNumberPagination, ),
        kwargs,
    )
