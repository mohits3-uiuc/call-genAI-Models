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
        
        # Build payload
        payload = {
            'messages': [{'role': 'user', 'content': [{'text': prompt}]}],
            'inferenceConfig': {
                'temperature': body.get('temperature', 0.7),
                'maxTokens': body.get('max_tokens', 1000)
            }
        }
        
        # Call invoke_model API
        response = bedrock.invoke_model(
            modelId=os.environ.get('MODEL_ID', 'amazon.nova-micro-v1:0'),
            body=json.dumps(payload)
        )
        
        # Parse response
        result = json.loads(response['body'].read())
        text = result['output']['message']['content'][0]['text']
        
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


# Test function
def test_invoke_model():
    """Test the invoke_model API function"""
    
    test_event = {
        'prompt': 'Explain the difference between AI and ML in simple terms',
        'temperature': 0.6,
        'max_tokens': 300
    }
    
    print("Testing invoke_model API...")
    print(f"Input: {test_event}")
    print("-" * 50)
    
    result = lambda_handler(test_event, None)
    print("Response:")
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    test_invoke_model()