# AWS Bedrock Lambda Functions - API Comparison

Two minimal Lambda functions for Amazon Bedrock Nova models using different APIs.

## Quick Overview

| Function | API | Lines | Best For |
|----------|-----|-------|----------|
| `bedrock-converse.py` | `converse()` | 35 | Chat apps, conversations |
| `bedrock-invoke-model.py` | `invoke_model()` | 38 | Direct calls, custom formatting |

## Setup

```bash
# Environment variables
export MODEL_ID=amazon.nova-micro-v1:0
export AWS_REGION=us-east-1

# Test locally
python bedrock-converse.py
python bedrock-invoke-model.py
```

## Request/Response (Both)

**Request:**
```json
{"prompt": "What is AI?", "temperature": 0.7, "max_tokens": 1000}
```

**Response:**
```json
{"statusCode": 200, "body": "{\"response\": \"AI is...\"}"}
```

## Key Differences

### Converse API
```python
response = bedrock.converse(
    modelId=model_id,
    messages=[{'role': 'user', 'content': [{'text': prompt}]}],
    inferenceConfig={'temperature': 0.7, 'maxTokens': 1000}
)
text = response['output']['message']['content'][0]['text']
```

### Invoke Model API
```python
payload = {'messages': [...], 'inferenceConfig': {...}}
response = bedrock.invoke_model(modelId=model_id, body=json.dumps(payload))
result = json.loads(response['body'].read())
text = result['output']['message']['content'][0]['text']
```

## Deployment

```bash
# Package
zip function.zip bedrock-converse.py

# Deploy
aws lambda update-function-code \
    --function-name my-function \
    --zip-file fileb://function.zip
```

## IAM Permissions

```json
{
    "Effect": "Allow",
    "Action": ["bedrock:InvokeModel", "bedrock:Converse"],
    "Resource": "*"
}
```

## When to Use

- **Converse**: Future-proof, cleaner API, conversation apps
- **Invoke Model**: More control, legacy support, custom payloads

Both functions are production-ready with identical input/output formats.