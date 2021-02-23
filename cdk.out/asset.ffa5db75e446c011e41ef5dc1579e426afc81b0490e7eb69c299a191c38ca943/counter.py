import json
import boto3
from pprint import pprint
from botocore.exceptions import ClientError
from decimal import Decimal

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("counter")
    response = table.scan()
    currentCount = response['Items'][0]['test']
    response2 = table.update_item(
        Key={
            'id': 2,
            'count': 2
        },
        UpdateExpression="SET test = test + :newValue",
        ExpressionAttributeValues={
            ':newValue': 1
        }
    )
    return currentCount