import streamlit as st
from streamlit_chat import message
from utils.utils import get_initial_message, get_chatgpt_response, update_chat
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("Chatbot : ChatGPT and Streamlit Chat")
st.subheader("AI Tutor:")

model = st.selectbox(
    "Select a model",
    ("gpt-3.5-turbo", "gpt-4")
)

# Initialize session states
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

query = st.text_input("Query: ", key="input")

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        
        # Debug information
        st.session_state['messages'] = messages
        
        response = get_chatgpt_response(messages, model)
        
        if response:  # Added error checking
            messages = update_chat(messages, "assistant", response)
            st.session_state.past.append(query)
            st.session_state.generated.append(response)
            st.session_state['messages'] = messages
        else:
            st.error("Failed to get response from the assistant")

# Display chat history
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)