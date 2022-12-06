import json
import os

import boto3

from boto3.dynamodb.conditions import Key
from decimal import Decimal

shoes_table_name = os.environ['TABLE']


def serialize_non_json(obj):
    if isinstance(obj, set):
        return list(obj)
    elif isinstance(obj, Decimal):
        return f'{obj.normalize():f}'

    return obj


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")
    table = dynamodb.Table(shoes_table_name)

    query_params = event["queryStringParameters"]

    brand = query_params.get("brand") if query_params else None

    if brand:
        response = table.query(KeyConditionExpression=Key('Brand').eq(brand), Limit=10)
    else:
        response = table.scan(Limit=10)

    items = response['Items']

    return {
        'statusCode': 200,
        'body': json.dumps(items, default=serialize_non_json)
    }


