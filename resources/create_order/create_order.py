import json
import boto3
import os

bucket_name = os.environ['BUCKET']
orders_table_name = os.environ['TABLE']


def send_file(event):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    file_key = event["ClientID"] + "_" + event["OrderID"]
    bucket.put_object(Body=json.dumps(event).encode('utf-8'), Key=file_key)


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb", region_name="eu-central-1")
    table = dynamodb.Table(orders_table_name)

    # we could validate body by two means:
    # 1. by defining model in API gateway
    # 2. using dataclass
    # we could also check if such shoes exist in Shoes table
    table.put_item(Item=event)

    send_file(event)
