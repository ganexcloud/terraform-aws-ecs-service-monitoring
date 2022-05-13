import json
import logging
import os
import re
#from botocore.vendored import requests
import requests


HOOK_URL = os.environ['WebhookUrl']
MESSENGER = os.environ['Messenger']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def handler(event, context):
    '''
        main handler
    '''

    # start logging
    logger.info(f'Recieved event: {event}')
    message = json.loads(event['Records'][0]['Sns']['Message'])

    # use data from logs
    aws_account_id = message.get('account', None)
    aws_region = message.get('region', None)
    event_time = message.get('time', None)
    pipeline = message.get('detail', {}).get('pipeline', None)
    state = message.get('detail', {}).get('state', None)

    # set the color depending on state
    color = '808080'
    if state == 'SUCCEEDED':
        color = '00ff00'
        status = 'succeeded'
        squadcast_status = "resolve"
    elif state == 'STARTED':
        color = '00bbff'
        status = 'started'
        squadcast_status = "trigger"
    elif state == 'FAILED':
        color = 'ff0000'
        status = 'failed'
        squadcast_status = "trigger"
    elif state == 'SUPERSEDED':
        color = '808080'
        status = 'superseded'
        squadcast_status = "resolve"
    else:
        color = '000000'

    if MESSENGER == 'slack':
        headers = {}
    elif MESSENGER == 'msteams':
        headers = {}
    elif MESSENGER == 'squadcast':
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    elif MESSENGER == 'discord':
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    else:
        color = '000000'

    pipeline_url = f'''https://{aws_region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline}/view?region={aws_region}'''

    # Slack
    if MESSENGER == 'slack':
        message_data = {
            'attachments': [
                {
                    "mrkdwn_in": ["text"],
                    'fallback': 'Pipeline Status',
                    'color': f"#{color}",
                    'author_icon': 'https://www.awsgeek.com/AWS-History/icons/AWS-CodePipeline.svg',
                    "text": f"CodePipeline {pipeline} {status} (<{pipeline_url}|Open>)"
                }
            ]
        }
    # Microsoft teams
    elif MESSENGER == 'msteams':
        message_data = {
            'summary': 'summary',
            '@type': 'MessageCard',
            '@context': 'https://schema.org/extensions',
            'themeColor': f"#{color}",
            'title': f'{pipeline}',
            'sections': [
                {
                    'facts': [
                        {'name': 'Account', 'value': aws_account_id},
                        {'name': 'Region', 'value': aws_region},
                        {'name': 'Event time (UTC)', 'value': date},
                        {'name': 'Stage', 'value': stage},
                        {'name': 'Action', 'value': action},
                        {'name': 'State', 'value': state}
                    ],
                    'markdown': 'true'
                }
            ],
            'potentialAction': {
                '@type': 'OpenUri', 'name': 'Open in AWS', 'targets': [
                    {'os': 'default', 'uri': pipeline_url}
                ]
            }
        }
    # Squadcast
    elif MESSENGER == 'squadcast':
        message_data = {
            "message": f"CodePipeline {pipeline} {status}",
            "description": f"**Pipeline:** {pipeline} \n**Status:** {status} \n**URL:** {pipeline_url} \n**Priority:** P5",
            "status": f"{squadcast_status}",
            "event_id": "6"
        }
    # Discord
    elif MESSENGER == 'discord':
        color = int(color, base=16)
        message_data = {
            'embeds': [
                {
                    "title": f"CodePipeline {pipeline} {status}",
                    "description": f"[Open]({pipeline_url})",
                    "color": color
                }
            ]
        }

    else:
        logger.info(f'Not support messenger {MESSENGER}')
        return

    # send message to webhook
    logger.debug(f'send message: {message_data}')
    res = requests.post(HOOK_URL, json.dumps(message_data), headers=headers)
    logger.debug(f'response: {res}')
    return
