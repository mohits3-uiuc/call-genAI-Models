import json
import os
import boto3

# Initialize Bedrock client
region = os.environ.get('AWS_REGION', 'us-east-1')
bedrock = boto3.client('bedrock-runtime', region_name=region)

def lambda_handler(event, context):
    try:
        # Parse input body
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        # Get prompt from request
        prompt = body.get('prompt', '')
        
        # Validate prompt
        if not prompt:
            error_response = {
                'statusCode': 400, 
                'body': json.dumps({'error': 'Prompt required'})
            }
            return error_response
        
        # Get optional parameters
        temperature = body.get('temperature', 0.7)
        max_tokens = body.get('max_tokens', 1000)
        
        # Build message for Nova model
        user_message = {
            "role": "user", 
            "content": [{"text": prompt}]
        }
        
        # Build inference config
        inference_config = {
            "temperature": temperature,
            "maxTokens": max_tokens
        }
        
        # Create payload for Bedrock
        payload = {
            "messages": [user_message],
            "inferenceConfig": inference_config
        }
        
        # Get model ID
        model_id = os.environ.get('MODEL_ID', 'amazon.nova-micro-v1:0')
        
        # Call Bedrock model
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(payload)
        )
        
        # Parse response
        response_body = response['body'].read()
        result = json.loads(response_body)
        
        # Extract generated text
        output = result['output']
        message = output['message']
        content = message['content'][0]
        text = content['text']
        
        # Build success response
        success_response = {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'response': text})
        }
        
        return success_response
        
    except Exception as e:
        # Build error response
        error_response = {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
        
        return error_response


# Test function for VS Code
def test_lambda():
    """Test the Lambda function locally"""
    
    # Sample test event
    test_event = {
        'body': json.dumps({
            'prompt': 'What is artificial intelligence?',
            'temperature': 0.7,
            'max_tokens': 500
        })
    }
    
    print("Testing Lambda function...")
    print(f"Input: {test_event}")
    print("-" * 50)
    
    # Call the lambda handler
    result = lambda_handler(test_event, None)
    
    print("Response:")
    print(json.dumps(result, indent=2))


# Run test when script is executed directly
if __name__ == '__main__':
    test_lambda()
