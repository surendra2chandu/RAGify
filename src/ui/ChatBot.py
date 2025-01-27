
#import necessary libraries
import streamlit as st
import requests
import sys
sys.path.append(r'C:\PycharmProjects\RAGify')
from src.utilities.LateChunkingServiceManager import get_response_late_chunking
from src.utilities.Tf_IdfServiceManager import get_response_tf_idf


container=st.container(height=120,border=True)
container.title("What assistance do you require?")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for buttons
with st.sidebar:
    contain = st.container(height=210, border=True)

    contain.title("**Retrival methods**")
    Late_Chunking_button = contain.button("Late Chunking")
    Tf_Idf_button = contain.button("Tf-Idf")

    con=st.container(height=210,border=True)
    con.title("**Content source**")
    web_content = con.button("Web Content")
    doc_content= con.button("Doc Content")

    refresh_button = st.button("🔄Refresh")
    if refresh_button:
        st.session_state.messages = []

    # Set the operation based on button clicks
if Late_Chunking_button:
    operation = "Late Chunking"
elif Tf_Idf_button:

    operation = "Tf-Idf"
else:
    operation = None




# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for query
if prompt := st.chat_input("Enter your query..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(f"***Question:*** {prompt}")

    # Process query and generate response
    try:
        if operation == "Late Chunking":

            # Get response from Late Chunking service
            response = get_response_late_chunking(prompt)

        elif operation == "Tf-Idf":
            # Get response from Tf-Idf service
            response = get_response_tf_idf(prompt)
        else:
            response = "Please select either Late Chunking or Tf-Idf to perform an operation."
    except Exception as e:
        response = f"There was an error while processing your request: {e}"

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(f"***Answer:*** {response}")

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

st.markdown(
    """
    <style>
            .stButton>button { width: 200px;   /* Set button width */height: 45px;   /* Set button height */font-size: 10px; /* Set button font size */}
     </style>

    """,
    unsafe_allow_html=True)
