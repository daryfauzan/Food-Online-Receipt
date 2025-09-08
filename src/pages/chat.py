import streamlit as st

from services.chat import run_agent

st.set_page_config(page_title="Chat with AI", page_icon="💬")

st.title("💬 Chat with AI")


# Keep chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
prompt = st.chat_input("Type your message...")
if prompt:
    # Add user message
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        reply = run_agent(prompt)
    except Exception as e:
        reply = f"Error: {e}"

    # Add assistant reply
    st.session_state["messages"].append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
