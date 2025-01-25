
#import necessary libraries
import streamlit as st
import requests
from sympy.printing.pretty.pretty_symbology import center

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
operation = None
if Late_Chunking_button:
    operation = "Late Chunking"
elif Tf_Idf_button:
    operation = "Tf-Idf"

# Main container


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
            url = "http://127.0.0.1:8002/retrieve_text/"
            response = requests.post(url, params={"query": prompt})
            if response.status_code == 200:
                response = response.json()
            else:
                response = f"Error occurred when processing the request to url {url}"
        elif operation == "Tf-Idf":
            url = "http://127.0.0.1:8002/tf-idf/"
            documents = [
                "The sun sets behind the mountains, casting a golden glow.",
                "The sun warmed the beach as we walked along the shore.",
                "She picked up her book and opened to the first page.",
                "After a long day, he relaxed with a hot cup of tea.",
                "The warmed air by the beach made the evening even more pleasant."
            ]
            response = requests.post(url, json={"corpus": documents, "query": prompt})
            if response.status_code == 200:
                response = response.json().get("response", "")
            else:
                response = f"Error occurred when processing the request to url {url}"
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
