import aws_cdk as core
import aws_cdk.assertions as assertions

from above_cdk.above_cdk_stack import AboveCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in above_cdk/above_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AboveCdkStack(app, "above-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
