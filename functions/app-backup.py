import os
import json
import logging
#import http.client
import requests

# ---------------------------------------------------------------------------------------------------------------------
# ENVIRONMENTAL VARIABLES
# ---------------------------------------------------------------------------------------------------------------------

# Boolean flag, which determins if the incoming even should be printed to the output.
LOG_EVENTS = os.getenv('LOG_EVENTS', 'False').lower() in ('true', '1', 't', 'yes', 'y')

#SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', '')
#if SLACK_WEBHOOK_URL == '':
#    raise RuntimeError('The required env variable SLACK_WEBHOOK_URL is not set or empty!')
#
HOOK_URL = os.environ['WebhookUrl']
MESSENGER = os.environ['Messenger']

# Set the log level
log = logging.getLogger()
log.setLevel(os.environ.get("LOG_LEVEL", "debug"))

# ---------------------------------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------------------------------------------------

# Get Event Source
def get_event_source(messenger, event: dict):
    if 'pathParameters' in event and 'proxy' in event['pathParameters']:
        return 'api_gateway_aws_proxy'
    if 'requestContext' in event and 'resourceId' in event['requestContext']:
        return 'api_gateway_http'
    elif 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:s3':
        return 's3'
    elif 'Records' in event and len(event['Records']) > 0 and 'EventSource' in event['Records'][0] and event['Records'][0]['EventSource'] == 'aws:sns':
        return 'sns'
    elif 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:dynamodb':
        return 'dynamo_db'
    elif 'Records' in event and len(event['Records']) > 0 and 'cf' in event['Records'][0]:
        return 'cloudfront'
    elif 'source' in event and event['source'] == 'aws.events':
        return 'scheduled_event'

    elif 'source' in event and event['source'] == 'aws.ecs':
        if messenger == 'slack':
            event_id = event.get('id')
            detail_type = event.get('detail-type')
            account = event.get('account')
            time = event.get('time')
            region = event.get('region')
            resources = []
            for resource in event['resources']:
                try:
                    resources.append(resource.split(':')[5])
                except Exception:
                    log.error('Error parsing the resource ARN: `{}`'.format(resource))
                    resources.append(resource)
            detail = event.get('detail')
            #known_detail = ecs_events_parser(detail_type, detail)
            blocks = list()
            contexts = list()
            title = f'*{detail_type}*'
            blocks.append(
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': title
                    }
                }
            )
            if resources:
                blocks.append(
                    {
                        'type': 'section',
                        'text': {
                            'type': 'mrkdwn',
                            'text': "*Resources*:\n" + '\n'.join(resources)
                        }
                    }
                )
            #if detail and not known_detail:
            #    blocks.append(
            #        {
            #            'type': 'section',
            #            'text': {
            #                'type': 'mrkdwn',
            #                'text': f'*Event Detail:* ```{json.dumps(detail, indent=4)}```'
            #            }
            #        }
            #    )
            #if known_detail:
            #    blocks.append(
            #        {
            #            'type': 'section',
            #            'text': {
            #                'type': 'mrkdwn',
            #                'text': known_detail
            #            }
            #        }
            #    )
            contexts.append({
                'type': 'mrkdwn',
                'text': f'Account: {account} Region: {region}'
            })
            contexts.append({
                'type': 'mrkdwn',
                'text': f'Time: {time} UTC Id: {event_id}'
            })
            blocks.append({
                'type': 'context',
                'elements': contexts
            })
            blocks.append({'type': 'divider'})
            return {'blocks': blocks}
        elif messenger == 'discord':
            event_id = event.get('id')
            detail_type = event.get('detail-type')
            account = event.get('account')
            time = event.get('time')
            region = event.get('region')
            resources = []
            for resource in event['resources']:
                try:
                    resources.append(resource.split(':')[5])
                except Exception:
                    log.error('Error parsing the resource ARN: `{}`'.format(resource))
                    resources.append(resource)
            detail = event.get('detail')
           # known_detail = ecs_events_parser(detail_type, detail)
            blocks = list()
            contexts = list()
            footer = list()
            title = f'*{detail_type}*'
            contexts.append({
                'name': 'Resources',
                'value': '\n'.join(resources)
            })
            contexts.append({
                'name': 'Details',
                #'value': known_detail
            })
            footer.append(
                {
                    'text': account
                }
            )
            blocks.append({
                'title': title,
                'fields': contexts,
                'footer': {
                    "text": f'Account: {account} | Region: {region}'
                }
            })
            return {'embeds': blocks}
    elif 'awslogs' in event and 'data' in event['awslogs']:
        return 'cloud_watch_logs'
    elif 'authorizationToken' in event and event['authorizationToken'] == "incoming-client-token":
        return 'api_gateway_authorizer'
    elif 'configRuleId' in event and 'configRuleName' in event and 'configRuleArn' in event:
        return 'aws_config'
    elif 'StackId' in event and 'RequestType' in event and 'ResourceType' in event:
        return 'cloud_formation'
    elif 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:codecommit':
        return 'code_commit'
    elif 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:ses':
        return 'ses'
    elif 'Records' in event and len(event['Records']) > 0 and 'eventSource' in event['Records'][0] and event['Records'][0]['eventSource'] == 'aws:kinesis':
        return 'kinesis'
    elif 'records' in event and len(event['Records']) > 0 and 'approximateArrivalTimestamp' in event['records'][0]:
        return 'kinesis_firehose'
    elif 'records' in event and len(event['Records']) > 0 and 'deliveryStreamArn' in event and event['deliveryStreamArn'] is str and event['deliveryStreamArn'].startswith('arn:aws:kinesis:'):
        return 'kinesis_firehose'
    elif 'eventType' in event and event['eventType'] == 'SyncTrigger' and 'identityId' in event and 'identityPoolId' in event:
        return 'cognito_sync_trigger'
    elif 'operation' in event and 'message' in event:
        return 'is_mobile_backend'

## Parse events
# ECS
#def ecs_events_parser(detail_type, detail):
#    if detail_type == 'ECS Container Instance State Change':
#        result = f'*Instance ID:* ' + detail['ec2InstanceId'] + '\n' + \
#                 '• Status: ' + detail['status']
#        if 'statusReason' in detail:
#            result = result + '\n' + '• Reason: ' + detail['statusReason']
#        return result
#
#    if detail_type == 'ECS Deployment State Change':
#        result = f'*Event Detail:*' + emoji_event_name.get(detail['eventName'], "") + '\n' + \
#                 '• ' + detail['eventType'] + ' - ' + detail['eventName'] + '\n' + \
#                 '• Deployment: ' + detail['deploymentId'] + '\n' + \
#                 '• Reason: ' + detail['reason']
#        return result
#
#    if detail_type == 'ECS Service Action':
#        result = f'*Event Detail:*' + emoji_event_name.get(detail['eventName'], "") + '\n' + \
#                 '• ' + detail['eventType'] + ' - ' + detail['eventName']
#        if 'capacityProviderArns' in detail:
#            capacity_providers = ""
#            for capacity_provider in detail['capacityProviderArns']:
#                try:
#                    capacity_providers = capacity_providers + capacity_provider.split(':')[5].split('/')[1] + ", "
#                except Exception:
#                    log.error('Error parsing clusterArn: `{}`'.format(capacity_provider))
#                    capacity_providers = capacity_providers + capacity_provider + ", "
#            if capacity_providers != "":
#                result = result + '\n' + '• Capacity Providers: ' + capacity_providers
#        return result
#
#    if detail_type == 'ECS Task State Change':
#        container_instance_id = "UNKNOWN"
#        if 'containerInstanceArn' in detail:
#            try:
#                container_instance_id = detail['containerInstanceArn'].split(':')[5].split('/')[2]
#            except Exception:
#                log.error('Error parsing containerInstanceArn: `{}`'.format(detail['containerInstanceArn']))
#                container_instance_id = detail['containerInstanceArn']
#        try:
#            task_definition = detail['taskDefinitionArn'].split(':')[5].split(
#                '/')[1] + ":" + detail['taskDefinitionArn'].split(':')[6]
#        except Exception:
#            log.error('Error parsing taskDefinitionArn: `{}`'.format(detail['taskDefinitionArn']))
#            task_definition = detail['taskDefinitionArn']
#        try:
#            task = detail['taskArn'].split(':')[5].split('/')[2]
#        except Exception:
#            log.error('Error parsing taskArn: `{}`'.format(detail['taskArn']))
#            task = detail['taskArn']
#        result = f'*Event Detail:* ' + '\n' + \
#                 '• Task Definition: ' + task_definition + '\n' + \
#                 '• Last: ' + detail['lastStatus'] + ' ' + '\n' + \
#                 '• Desired: ' + detail['desiredStatus'] + ' '
#        if container_instance_id != "UNKNOWN":
#            result = result + '\n' + '• Instance ID: ' + container_instance_id
#        if detail['lastStatus'] == 'RUNNING':
#            if 'healthStatus' in detail:
#                result = result + '\n' + '• HealthStatus: ' + detail['healthStatus']
#        if detail['lastStatus'] == 'STOPPED':
#            if 'stopCode' in detail:
#                result = result + '\n' + '• Stop Code: ' + detail['stopCode']
#            if 'stoppedReason' in detail:
#                result = result + '\n' + '• Stop Reason: ' + detail['stoppedReason']
#        return result
#    return f'*Event Detail:* ```{json.dumps(detail, indent=4)}```'


# Input: EventBridge Message
#def slack(event):
#    event_id = event.get('id')
#    detail_type = event.get('detail-type')
#    account = event.get('account')
#    time = event.get('time')
#    region = event.get('region')
#    resources = []
#    for resource in event['resources']:
#        try:
#            resources.append(resource.split(':')[5])
#        except Exception:
#            log.error('Error parsing the resource ARN: `{}`'.format(resource))
#            resources.append(resource)
#    detail = event.get('detail')
#    known_detail = ecs_events_parser(detail_type, detail)
#    blocks = list()
#    contexts = list()
#    title = f'*{detail_type}*'
#    blocks.append(
#        {
#            'type': 'section',
#            'text': {
#                'type': 'mrkdwn',
#                'text': title
#            }
#        }
#    )
#    if resources:
#        blocks.append(
#            {
#                'type': 'section',
#                'text': {
#                    'type': 'mrkdwn',
#                    'text': "*Resources*:\n" + '\n'.join(resources)
#                }
#            }
#        )
#    if detail and not known_detail:
#        blocks.append(
#            {
#                'type': 'section',
#                'text': {
#                    'type': 'mrkdwn',
#                    'text': f'*Event Detail:* ```{json.dumps(detail, indent=4)}```'
#                }
#            }
#        )
#    if known_detail:
#        blocks.append(
#            {
#                'type': 'section',
#                'text': {
#                    'type': 'mrkdwn',
#                    'text': known_detail
#                }
#            }
#        )
#    contexts.append({
#        'type': 'mrkdwn',
#        'text': f'Account: {account} Region: {region}'
#    })
#    contexts.append({
#        'type': 'mrkdwn',
#        'text': f'Time: {time} UTC Id: {event_id}'
#    })
#    blocks.append({
#        'type': 'context',
#        'elements': contexts
#    })
#    blocks.append({'type': 'divider'})
#    return {'blocks': blocks}

#def discord(event):
#    event_id = event.get('id')
#    detail_type = event.get('detail-type')
#    account = event.get('account')
#    time = event.get('time')
#    region = event.get('region')
#    resources = []
#    for resource in event['resources']:
#        try:
#            resources.append(resource.split(':')[5])
#        except Exception:
#            log.error('Error parsing the resource ARN: `{}`'.format(resource))
#            resources.append(resource)
#    detail = event.get('detail')
#    known_detail = ecs_events_parser(detail_type, detail)
#    blocks = list()
#    contexts = list()
#    footer = list()
#    title = f'*{detail_type}*'
#    contexts.append({
#        'name': 'Resources',
#        'value': '\n'.join(resources)
#    })
#    contexts.append({
#        'name': 'Details',
#        'value': known_detail
#    })
#    footer.append(
#        {
#            'text': account
#        }
#    )
#    blocks.append({
#        'title': title,
#        'fields': contexts,
#        'footer': {
#            "text": f'Account: {account} | Region: {region}'
#        }
#    })
#    return {'embeds': blocks}

# Post Webhook
def post(hook_url, message):
    log.debug(f'Sending message: {json.dumps(message)}')
    headers = {'Content-type': 'application/json'}
    response = requests.post(HOOK_URL, json.dumps(message), headers=headers)
    log.debug('Response: {}, message: {}'.format(response.status_code, response.text))
    return response.status_code

def lambda_handler(event, context):
    if LOG_EVENTS:
        log.info('Event logging enabled: `{}`'.format(json.dumps(event)))

    if MESSENGER in ('slack', 'discord', 'squadcast'):
        message = get_event_source(MESSENGER, event)
        response = post(HOOK_URL, message)
        if response != 200:
            log.error(
                "Error: received status `{}` using event `{}` and context `{}`".format(response, event,
                                                                                       context))
        return json.dumps({"code": response})

    else:
        raise ValueError(f'Not support messenger {MESSENGER}')

# For local testing
if __name__ == '__main__':
    with open('./test/eventbridge_event.json') as f:
        test_event = json.load(f)
    lambda_handler(test_event, "default_context")
