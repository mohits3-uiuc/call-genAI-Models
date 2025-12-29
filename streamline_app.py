import streamlit as st
import requests
import json

# Configure Streamlit page
st.set_page_config(
    page_title="AI Chat with Amazon Bedrock Nova",
    page_icon="🤖",
    layout="centered"
)

# API Gateway URL
API_GATEWAY_URL = "https://x76yo5qxzc.execute-api.us-east-1.amazonaws.com/DEV/call-bedrock-converse-api"

def call_bedrock_api(prompt, temperature=0.7, max_tokens=1000):
    """
    Call the API Gateway endpoint which triggers Lambda function to call Bedrock
    """
    try:
        # Prepare the request payload
        payload = {
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        # Make the API call
        response = requests.post(
            API_GATEWAY_URL,
            json=payload,
            headers={
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse the response - API Gateway returns Lambda proxy format
        result = response.json()
        
        # Handle Lambda proxy integration response format
        if "body" in result and isinstance(result["body"], str):
            # The actual response is in the body field as a JSON string
            body = json.loads(result["body"])
            return body.get("response", "No response received"), None
        elif "response" in result:
            # Direct response format
            return result.get("response", "No response received"), None
        else:
            # Fallback - try to find response in the result
            return result.get("response", f"Unexpected response format: {result}"), None
        
    except requests.exceptions.RequestException as e:
        return None, f"API Request Error: {str(e)}"
    except json.JSONDecodeError as e:
        return None, f"JSON Decode Error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected Error: {str(e)}"

# Streamlit UI
st.title("🤖 AI Chat with Amazon Bedrock Nova")
st.markdown("Enter your question or prompt below to interact with Amazon Nova AI model via API Gateway → Lambda → Bedrock")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, help="Controls randomness in responses")
    max_tokens = st.slider("Max Tokens", 100, 4000, 1000, 100, help="Maximum length of response")
    
    st.markdown("---")
    st.markdown("**API Endpoint:**")
    st.code(API_GATEWAY_URL, language="text")

# Main chat interface
prompt = st.text_area(
    "Enter your prompt:",
    height=100,
    placeholder="Ask me anything... e.g., 'Explain quantum computing in simple terms'"
)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Response area
if st.button("🚀 Send Request", type="primary"):
    if prompt.strip():
        with st.spinner("Calling API Gateway → Lambda → Bedrock..."):
            # Call the API
            response, error = call_bedrock_api(prompt, temperature, max_tokens)
            
            if error:
                st.error(f"❌ Error: {error}")
            else:
                st.success("✅ Response received!")
                st.markdown("### 🤖 AI Response:")
                st.markdown(response)
                
                # Add to chat history
                st.session_state.chat_history.append((prompt, response))
    else:
        st.warning("⚠️ Please enter a prompt before sending the request.")

# Display previous conversations
if st.session_state.chat_history:
    st.markdown("---")
    st.markdown("### 📝 Chat History")
    for i, (user_prompt, ai_response) in enumerate(st.session_state.chat_history[-5:]):  # Show last 5
        with st.expander(f"Conversation {len(st.session_state.chat_history) - i}"):
            st.markdown(f"**You:** {user_prompt}")
            st.markdown(f"**AI:** {ai_response}")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <small>
            This app connects to AWS API Gateway → Lambda → Amazon Bedrock Nova Model<br>
            Built with Streamlit 🎈
        </small>
    </div>
    """,
    unsafe_allow_html=True
)
