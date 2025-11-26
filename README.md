# AWS Lambda Function for Amazon Bedrock (Nova Model)

A simple and clean AWS Lambda function to call Amazon's Nova generative AI model via Bedrock API.

## Features

- ✅ **Easy to read code** - Simple, well-commented Python code
- ✅ **Amazon Nova Model** - Optimized for Nova model format
- ✅ **Environment configuration** - Configurable via environment variables
- ✅ **API Gateway ready** - CORS support and proper HTTP responses
- ✅ **Local testing** - Test function included for VS Code development
- ✅ **Error handling** - Comprehensive error handling with proper status codes

## Quick Start

### 1. Prerequisites
- AWS Account with Bedrock access
- Python 3.8+ 
- AWS CLI configured (`aws configure`)
- Access to Amazon Nova models in Bedrock

### 2. Local Testing
```bash
# Run directly in VS Code or terminal
python bedrock-lambda.py
```

### 3. Deploy to AWS Lambda
1. Create a new Lambda function in AWS Console
2. Upload `bedrock-lambda.py` as your function code
3. Set environment variables (see configuration below)
4. Attach IAM role with Bedrock permissions

## Configuration

### Environment Variables
```bash
MODEL_ID=amazon.nova-micro-v1:0    # Nova model to use
AWS_REGION=us-east-1               # AWS region
```

### IAM Permissions
Your Lambda execution role needs:
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }
    ]
}
```

## API Usage

### Request Format
```json
{
    "prompt": "Your question or prompt here",
    "temperature": 0.7,    // Optional: 0.0-1.0 (creativity level)
    "max_tokens": 1000     // Optional: Response length limit
}
```

### Response Format
```json
{
    "statusCode": 200,
    "headers": {
        "Access-Control-Allow-Origin": "*"
    },
    "body": "{\"response\": \"AI generated response here\"}"
}
```

## Examples

### Direct Lambda Invocation
```python
import json
from bedrock_lambda import lambda_handler

event = {
    "prompt": "What is artificial intelligence?",
    "temperature": 0.5,
    "max_tokens": 500
}

result = lambda_handler(event, None)
print(json.dumps(result, indent=2))
```

### API Gateway Event
```python
event = {
    "body": json.dumps({
        "prompt": "Explain quantum computing",
        "temperature": 0.7,
        "max_tokens": 800
    })
}

result = lambda_handler(event, None)
```

### cURL Example (after API Gateway setup)
```bash
curl -X POST https://your-api-gateway-url/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short poem about AI",
    "temperature": 0.8,
    "max_tokens": 300
  }'
```

## Parameter Guide

### Temperature
- **0.1-0.3**: Focused, deterministic (good for facts, code)
- **0.4-0.7**: Balanced (good for general chat)
- **0.8-1.0**: Creative, varied (good for creative writing)

### Max Tokens
- **300 tokens**: ~225 words (short answer)
- **500 tokens**: ~375 words (paragraph)
- **1000 tokens**: ~750 words (detailed response)
- **2000 tokens**: ~1500 words (long response)

## Error Handling

The function handles various error scenarios:

- **400**: Missing prompt
- **500**: Bedrock API errors, JSON parsing errors
- **CORS**: Proper CORS headers for web applications

## File Structure
```
bedrock-lambda.py          # Main Lambda function
README.md                  # This file
```

## Development

### Testing Locally
1. Make sure AWS credentials are configured
2. Run the test function:
```bash
python bedrock-lambda.py
```

### Modifying Test Data
Edit the `test_lambda()` function to try different prompts:
```python
test_event = {
    'body': json.dumps({
        'prompt': 'Your custom prompt here',
        'temperature': 0.5,
        'max_tokens': 200
    })
}
```

## Deployment Options

### 1. AWS Console
- Upload the Python file directly
- Set environment variables in Configuration tab

### 2. AWS CLI
```bash
# Create deployment package
zip function.zip bedrock-lambda.py

# Update Lambda function
aws lambda update-function-code \
    --function-name your-function-name \
    --zip-file fileb://function.zip
```

### 3. Infrastructure as Code
Can be deployed with CloudFormation, CDK, or Terraform.

## Cost Considerations

- **Lambda**: Pay per invocation and execution time
- **Bedrock**: Pay per input/output tokens
- **API Gateway**: Pay per API call (if used)

Monitor usage in AWS CloudWatch and set up billing alerts.

## Troubleshooting

### Common Issues

1. **"Access denied to Bedrock"**
   - Check IAM permissions
   - Verify Bedrock is available in your region

2. **"Model not found"**
   - Check MODEL_ID environment variable
   - Verify you have access to the specific Nova model

3. **"JSON parsing error"**
   - Check request body format
   - Ensure prompt is provided

### Debugging
Check CloudWatch logs for detailed error messages:
```bash
aws logs tail /aws/lambda/your-function-name --follow
```

## Support

For issues related to:
- **AWS Lambda**: AWS Documentation
- **Amazon Bedrock**: AWS Bedrock Documentation  
- **This code**: Check the comments in `bedrock-lambda.py`

## License

This code is provided as-is for educational and development purposes.