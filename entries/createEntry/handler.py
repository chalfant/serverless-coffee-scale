from __future__ import print_function

import json
import logging
import boto3
import os

log = logging.getLogger()
log.setLevel(logging.DEBUG)

table_name = os.getenv('DYNAMODB_TABLE_NAME')
ddb = boto3.resource('dynamodb')
table = ddb.Table(table_name)

def handler(event, context):
    log.debug("Received event {}".format(json.dumps(event)))

    scale_id  = event['scale_id']
    timestamp = event['timestamp']
    weight    = event['weight']

    item = {
        'scale_id': scale_id,
        'timestamp': timestamp,
        'weight': weight
    }

    response = table.put_item(
        Item=item
    )

    return item
