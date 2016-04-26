from __future__ import print_function

import json
import logging
import boto3
from boto3.dynamodb.conditions import Key, Attr
import os

log = logging.getLogger()
log.setLevel(logging.DEBUG)

table_name = os.getenv('DYNAMODB_TABLE_NAME')
ddb = boto3.resource('dynamodb')
table = ddb.Table(table_name)

def query_entries(table, scale_id, start_time, end_time):
    results = []
    response = table.query(
        KeyConditionExpression=Key('scale_id').eq(scale_id) & Key('timestamp').between(start_time, end_time)
    )
    for item in response['Items']:
        results.append(item)

    while 'LastEvaluatedKey' in response:
        logger.debug('query next chunk starting at {}'.format(json.dumps(response['LastEvaluatedKey'])))
        response = table.query(
            ExclusiveStartKey=response['LastEvaluatedKey'],
            KeyConditionExpression=Key('scale_id').eq(scale_id) & Key('timestamp').between(start_time, end_time)
        )
        for item in response['Items']:
            results.append(item)

    return results

def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    scale_id   = event['scale_id']
    start_time = event['start_time']
    end_time   = event['end_time']

    entries = query_entries(table, scale_id, start_time, end_time)

    return {'entries': entries}
