from schema import Schema

create_response_schema = Schema(
    {
        'id': int,
        'created_at': str,
    }
)

token_schema = Schema(
    {
        'access': str,
        'refresh': str,
    }
)

account_book_schema = Schema(
    {
        'id': int,
        'created_at': str,
        'updated_at': str,
        'name': str,
    }
)
