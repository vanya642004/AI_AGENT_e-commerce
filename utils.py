def clean_sql_result(result):
    if isinstance(result, list):
        return [dict(row) for row in result]
    return result
