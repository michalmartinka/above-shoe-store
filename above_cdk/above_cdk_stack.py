from aws_cdk import Stack
from constructs import Construct

from above_cdk.store_service import ShoeStoreService


class AboveCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ShoeStoreService(self, "ShoeStore")
