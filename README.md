# AWS Lambda for Amazon Bedrock Nova Model

Simple Lambda function to call Amazon Nova AI models via Bedrock API.

## Quick Start

```bash
# Test locally
python bedrock-lambda.py

# Deploy to AWS Lambda
zip function.zip bedrock-lambda.py
aws lambda update-function-code --function-name my-function --zip-file fileb://function.zip
```

## Configuration

**Environment Variables:**
```bash
MODEL_ID=amazon.nova-micro-v1:0
AWS_REGION=us-east-1
```

**IAM Permission:**
```json
{"Effect": "Allow", "Action": ["bedrock:InvokeModel"], "Resource": "*"}
```

## Usage

**Request:**
```json
{"prompt": "What is AI?", "temperature": 0.7, "max_tokens": 1000}
```

**Response:**
```json
{"statusCode": 200, "body": "{\"response\": \"AI is...\"}"}
```

## Parameters

- **temperature**: 0.1 (focused) → 1.0 (creative)
- **max_tokens**: 300 (~225 words) → 2000 (~1500 words)

## API Gateway Example

```bash
curl -X POST https://api-url/invoke \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing"}'
```

## Streamlit Web Application

A user-friendly web interface to interact with the Bedrock API via API Gateway.

**Quick Start:**
```bash
# Install dependencies and run the app
./run_app.sh

# Or run manually
pip install -r requirements.txt
streamlit run streamlit_app.py
```

**Features:**
- Interactive chat interface
- Configurable temperature and max tokens
- Real-time API calls to your API Gateway
- Chat history tracking
- Error handling and status display

**Access:** Open http://localhost:8501 in your browser

## Files

- `bedrock-lambda.py` - Main Lambda function (clean, readable code)
- `bedrock-converse.py` - Alternative using converse API
- `bedrock-invoke-model.py` - Alternative using invoke_model API
- `streamlit_app.py` - Streamlit web application
- `requirements.txt` - Python dependencies
- `run_app.sh` - Quick start script
- `README-APIs.md` - Detailed API comparison guide

## Troubleshooting

- **Access denied**: Check IAM permissions and Bedrock region availability
- **Model not found**: Verify MODEL_ID and model access
- **API Gateway timeout**: Check Lambda function timeout settings
- **CORS errors**: Ensure proper CORS headers in Lambda response
- **Logs**: `aws logs tail /aws/lambda/function-name --follow`
