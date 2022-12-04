import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_s3 as s3,
                     aws_lambda as lambda_,
                     aws_dynamodb as dynamodb)


class ShoeStoreService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        bucket = s3.Bucket(self, "OrdersBucket")

        shoes_table = dynamodb.Table(self, "ShoesTable",
                                     partition_key=dynamodb.Attribute(name="Brand", type=dynamodb.AttributeType.STRING),
                                     sort_key=dynamodb.Attribute(name="Reference", type=dynamodb.AttributeType.STRING),
                                     billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST)

        orders_table = dynamodb.Table(self, "OrdersTable",
                                      partition_key=dynamodb.Attribute(name="ClientID",
                                                                       type=dynamodb.AttributeType.STRING),
                                      sort_key=dynamodb.Attribute(name="OrderID", type=dynamodb.AttributeType.STRING),
                                      billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST)

        shoes_handler = lambda_.Function(self, "ShoesHandler",
                                         runtime=lambda_.Runtime.PYTHON_3_9,
                                         code=lambda_.Code.from_asset("resources/get_shoes"),
                                         handler="get_shoes.lambda_handler",
                                         environment=dict(
                                             TABLE=shoes_table.table_name,
                                             BUCKET=bucket.bucket_name)
                                         )

        orders_handler = lambda_.Function(self, "OrdersHandler",
                                          runtime=lambda_.Runtime.PYTHON_3_9,
                                          code=lambda_.Code.from_asset("resources/create_order"),
                                          handler="create_order.lambda_handler",
                                          environment=dict(
                                              TABLE=orders_table.table_name,
                                              BUCKET=bucket.bucket_name)
                                          )

        shoes_table.grant_read_data(shoes_handler)

        orders_table.grant_write_data(orders_handler)
        bucket.grant_write(orders_handler)

        api = apigateway.RestApi(self, "shoes-store-api",
                                 rest_api_name="Shoe Store API",
                                 description="Shoes store api")

        shoes_integration = apigateway.LambdaIntegration(shoes_handler,
                                                         request_templates={
                                                             "application/json": '{ "statusCode": "200" }'})

        orders_integration = apigateway.LambdaIntegration(orders_handler,
                                                          request_templates={
                                                              "application/json": '{ "statusCode": "200" }'})

        shoes_resource = api.root.add_resource("shoes")
        orders_resource = api.root.add_resource("orders")

        shoes_resource.add_method("GET", shoes_integration)
        orders_resource.add_method("POST", orders_integration)
