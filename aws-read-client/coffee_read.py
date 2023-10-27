import imp
import boto3
import pprint

session = boto3.Session()
query_client = session.client('timestream-query')
paginator = query_client.get_paginator('query')
page_iterator = paginator.paginate(
    QueryString=f"SELECT measure_value::varchar FROM linkaffe.kannvikt",
    PaginationConfig={'MaxItems': 10}
)

for page in page_iterator:
    pprint.pprint(page)
