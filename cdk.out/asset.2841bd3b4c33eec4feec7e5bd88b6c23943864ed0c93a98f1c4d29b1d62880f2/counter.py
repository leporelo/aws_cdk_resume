import json
import boto3
import os
from pprint import pprint
from botocore.exceptions import ClientError
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # print('request: {}'.format(json.dumps(event)))
    print(event["path"])
    
    table = dynamodb.Table(os.environ['TABLE_NAME'])
    response2 = table.update_item(
        Key={
            'id': event['path']
        },
        UpdateExpression='ADD hits :newValue',
        ExpressionAttributeValues={':newValue': 1})
    
    response = table.scan()
    currentCount = response['Items'][0]['hits']
    return {
        "statusCode": 200,
        "body": json.dumps(event["path"]),
        "headers":{ 'Access-Control-Allow-Origin' : '*' }
        }