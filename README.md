# Text-to-Speech Conversion Solution

This repository contains an AWS serverless solution for converting text to speech. The solution leverages services such as API Gateway, Lambda, DynamoDB, Amazon Polly, SNS, S3, and SES for efficient and scalable implementation.

# Features

- **API Gateway**: Receives a POST request with the text, user's email, and voice preference (male/female).

- **Lambda Functions**:

  + new-text: Stores request data in DynamoDB and publishes a message on an SNS topic.

  + text2speech: Subscribes to the SNS topic, processes the message, invokes Amazon Polly for text-to-speech conversion, stores the audio file in S3, generates a pre-signed URL for the audio file and invokes SES to send an email to the user's email along with the pre-signed URL

- **DynamoDB**: Stores details of user requests.

- **Amazon Polly**: Converts the provided text to speech.

- **Amazon S3**: Stores the converted audio file and generates a pre-signed URL.

- **Amazon SES**: Sends the pre-signed URL to the user's email address.

# Architecture Diagram

![text2speech_aws drawio (1)](https://github.com/user-attachments/assets/6f6ae759-e631-4887-b418-49d0a1359085)
