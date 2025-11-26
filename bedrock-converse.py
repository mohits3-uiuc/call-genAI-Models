import json
import os
import boto3

bedrock = boto3.client('bedrock-runtime', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

def lambda_handler(event, context):
    try:
        # Parse input
        body = json.loads(event['body']) if 'body' in event else event
        prompt = body.get('prompt', '')
        
        if not prompt:
            return {'statusCode': 400, 'body': json.dumps({'error': 'Prompt required'})}
        
        # Build message
        messages = [{'role': 'user', 'content': [{'text': prompt}]}]
        
        # Call converse API
        response = bedrock.converse(
            modelId=os.environ.get('MODEL_ID', 'amazon.nova-micro-v1:0'),
            messages=messages,
            inferenceConfig={
                'temperature': body.get('temperature', 0.7),
                'maxTokens': body.get('max_tokens', 1000)
            }
        )
        
        # Extract text
        text = response['output']['message']['content'][0]['text']
        
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'response': text})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }


# Simple test function
def test():
    event = {'prompt': 'What is AI?'}
    result = lambda_handler(event, None)
    print(result)


if __name__ == '__main__':
    test()