import json
import boto3
import time
sns = boto3.client('sns')
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    message_body = json.loads(event["Records"][0]["body"])
    
    
    
    object = s3.Object('complaints101', 'complaints/'+ message_body["UserInfo"]["username"] + "-" + str(time.time())+ ".json")
    object.put(Body=json.dumps(message_body).encode("utf-8"))
    
    
    message = "Subject: " + message_body["Subject"] + "\n" + "Description: " + message_body["Description"] + "\n" + "Type: " + message_body["Type"] +"\n" + "User Contact Details:" + "\n" + message_body["UserInfo"]["username"] + "\n" + message_body["UserInfo"]["email"] + "\n" + message_body["UserInfo"]["phone"] + "\n" + message_body["UserInfo"]["Address"]
    
    response = sns.publish(
        TopicArn = 'arn:aws:sns:us-east-2:404444578694:Complaints',
        Message = message,
        Subject = 'New Complaint'
    )
    
    return {
        'statusCode': 200,
        'body': message
    }
