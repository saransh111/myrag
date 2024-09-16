import streamlit as st
import requests

# Set up the API endpoint
api_endpoint = "http://127.0.0.1:8000/my_answers"

# Initialize chat history
st.title("My Mahatma gandhi,Maulana Azad Based RAG") 

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("What do you want to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send request to API
    my_context=""
    for messages in st.session_state.messages:
        my_context+=messages["content"]
    response = requests.post(api_endpoint, json={"query": prompt,"my_current_context" : my_context})
    if response.status_code == 200:
        my_response = response.json()["answer"]
        # split_string = api_response.split("Answer")
        # my_response= "\n".join(split_string)
        # split_string = my_response.split("context")
        # my_response=split_string[2]
        # Add API response to chat history
        st.session_state.messages.append({"role": "assistant", "content": my_response})

        # Display API response
        with st.chat_message("assistant"):
            st.markdown(my_response)
    else:
        st.error("Error communicating with the API.")