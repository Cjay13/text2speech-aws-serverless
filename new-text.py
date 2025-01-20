import json
import boto3
import uuid
import os

def lambda_handler(event, context):

    dynamodb = os.getenv('DYNAMODB_TABLE')


    dynamodb = boto3.resource('dynamodb')
    table_name = 'text2speech'
    table = dynamodb.Table(table_name)

    message = json.loads(event['body'])

    text = message.get('text', '')
    email = message.get('email', '')
    choice_of_voice = message.get('choice_of_voice', '')

    user_id = str(uuid.uuid4())

    table.put_item(
        Item={
            'user_id': user_id,
            'text': text,
            'email': email,
            'choice_of_voice': choice_of_voice
        }
    )

    sns_client = boto3.client('sns')

    sns_topic_arn = os.getenv('SNS_TOPIC_ARN')

    sns_message = {
        'user_id': user_id,
        'text': text,
        'email': email,
        'choice_of_voice': choice_of_voice
    }

    response = sns_client.publish(
        TopicArn=sns_topic_arn,
        Message=json.dumps(sns_message)
    )

    combined_message = "Thanks for your request. Your text will be converted into voice."

    return {
        'statusCode': 200,
        'body': json.dumps(combined_message)
    }
