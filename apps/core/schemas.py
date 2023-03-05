from schema import Or, Schema


def wrap_pagination_schema(item_schema):
    return Schema(
        {
            'count': int,
            'next': Or(str, None),
            'previous': Or(str, None),
            'results': [item_schema],
        }
    )


create_response_schema = Schema(
    {
        'id': int,
        'created_at': str,
    }
)

user_schema = Schema(
    {
        'id': int,
        'email': str,
    }
)

token_schema = Schema(
    {
        'access': str,
        'refresh': str,
        'user': user_schema,
    }
)

account_book_schema = Schema(
    {
        'id': int,
        'created_at': str,
        'updated_at': str,
        'name': str,
        'total_amount': int,
    }
)

transaction_schema = Schema(
    {
        'id': int,
        'created_at': str,
        'updated_at': str,
        'description': str,
        'amount': int,
        'type': str,
        'occurred_at': str,
    }
)

guest_schema = Schema(
    {
        'code': str,
        'created_at': str,
        'updated_at': str,
        'object_pks': {str: int},
        'access_scope': str,
        'expired_at': str,
        'is_expired': bool,
        'created_by': int,
    }
)
