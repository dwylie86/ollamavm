import streamlit as st
import json
import requests


def query_ollama(prompt, model="codellama"):
    """Send a query to Ollama and return the response"""
    url = "http://localhost:11434/api/generate"

    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()['response']
    return "Error: Could not get response from Ollama"


# Set up the Streamlit page
st.title("Ollama Chat Interface")

# Model selection
model = st.selectbox(
    "Choose your model",
    ["codellama", "mistral"]
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant response
    with st.chat_message("assistant"):
        response = query_ollama(prompt, model)
        st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a clear button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()