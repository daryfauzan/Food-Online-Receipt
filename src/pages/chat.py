import requests
import streamlit as st

st.set_page_config(page_title="Chat with AI", page_icon="💬")

st.title("💬 Chat with AI")

API_URL = "http://localhost:8000/chat"  # Replace with your API

# Keep chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        response = requests.post(API_URL, json={"message": prompt})
        if response.status_code == 200:
            reply = response.json().get("reply", "No response")
        else:
            reply = f"Error: {response.status_code}"
    except Exception as e:
        reply = f"Error: {e}"

    # Add assistant reply
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
