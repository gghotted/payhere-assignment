from schema import Schema

create_response_schema = Schema(
    {
        'id': int,
        'created_at': str,
    }
)
