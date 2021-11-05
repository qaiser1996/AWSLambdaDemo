import json
import boto3

def dispatchToSQS(qName, message):
    sqs = boto3.client('sqs')
    queue_url = sqs.get_queue_url(QueueName=qName).get('QueueUrl')
    resp = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=(
            message
        )
    )
    
def getUser(table_name, username):
    client = boto3.resource('dynamodb')
    table = client.Table(table_name)
    response = table.get_item(
        Key={
            'username': username
        }
    )

    return response["Item"]

def lambda_handler(event, context):
    try:
        username = event["headers"]["Username"]
        message_body = json.loads(event["body"])
        if not ("Subject" in message_body and "Description" in message_body and "Type" in message_body):
            raise("Invalid Payload")
            
        getUser("User",username)
        message_body["UserInfo"] = getUser("User",username)
        
        dispatchToSQS("complaintsQ", json.dumps(message_body))
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                "message":"Complaint has been registered, Complaint Center will get in touch with you shortly!"
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({
                "message":"Due to Technical Error, Complaint Could not be registered!"
            })
        }
