import json
import logging
import boto3
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

polly_client = boto3.client('polly')

def email_url(to_email, pre_signed_url):
    ses_client = boto3.client('ses')
    sender_email = os.getenv("SENDER_EMAIL)
    subject = "Your Audio File is Ready"
    Body = body = f"""
    Hello,

    Your requested file is ready for download. You can access it using the following link:

    {pre_signed_url}

    This link will expire in 1 hour. Please download the file before the expiration time.

    Best regards,
    CjayDevOps
    """

    try:
        response = ses_client.send_email(
            Source=sender_email,
            Destination={
                'ToAddresses': [to_email],
            },
            Message={
                'Subject': {
                    'Data': subject,
                },
                'Body': {
                    'Text': {
                        'Data': body,
                    },
                },
            },
        )

        logger.info(f"Email sent successfully: {response}")

    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def lambda_handler(event, context):
    for record in event['Records']:
        sns_message = record['Sns']['Message']
        logger.info(f"Received message: {sns_message}")
        try:
            parsed_message = json.loads(sns_message)  # Convert string to dict
            uuid = parsed_message.get("user_id", "No UUID provided")
            text = parsed_message.get("text", "No text provided")
            email = parsed_message.get("email", "No email provided")
            choice_of_voice = parsed_message.get("choice_of_voice", "No voice gender provided")

            logger.info(f"Extracted text: {text}")
            logger.info(f"Extracted email: {email}")
            logger.info(f"Extracted voice gender: {choice_of_voice}")

            if choice_of_voice == "male":
                voice_id = "Matthew"
            else:
                voice_id = "Joanna"

            response = polly_client.synthesize_speech(VoiceId=voice_id, OutputFormat="mp3", Text=text)

            audio_stream = response.get("AudioStream")
            if audio_stream:
                s3_client = boto3.client('s3')
                bucket_name = os.getenv("BUCKET_NAME")
                object_key = f"{uuid}.mp3"
                s3_client.put_object(Bucket=bucket_name, Key=object_key, Body=audio_stream.read())
                audio_file = s3_client.get_object(Bucket=bucket_name, Key=object_key)
                pre_signed_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': object_key}, ExpiresIn=3600)
                logger.info(f"Audio stream saved to S3 bucket: {bucket_name}, Key: {object_key}")
                email_url(email, pre_signed_url)

            else:
                logger.error("Failed to get audio stream from Polly response")


        except json.JSONDecodeError:
            logger.error("Failed to parse SNS message as JSON")
            continue



