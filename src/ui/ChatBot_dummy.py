import streamlit as st
import requests

st.title("Chat Bot")

documents = [
        "The sun sets behind the mountains, casting a golden glow.",
        "The sun warmed the beach as we walked along the shore.",
        "She picked up her book and opened to the first page.",
        "After a long day, he relaxed with a hot cup of tea.",
        "The warmed air by the beach made the evening even more pleasant."
    ]


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create two buttons for "Square" and "Cube" directly above the user input
col1, col2 = st.columns([1, 1])  # Creates two columns with equal width
with col1:
    square_button = st.button("Late Chunking")
with col2:
    cube_button = st.button("Tf-Idf")

# Initialize operation as None
operation = None

# Set the operation based on button clicks
if square_button:
    operation = "Late Chunking"
elif cube_button:
    operation = "Tf-Idf"

# User input for number, directly below the buttons
if prompt := st.chat_input("Enter your query..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Check if the user input is a number and return square or cube based on selection
    try:
        # Attempt to convert the input to a number
        if operation == "Late Chunking":
            url = "http://127.0.0.1:8002/retrieve_text/"

            response = requests.post(url, params={"query": prompt})

            if response.status_code == 200:
                response = response.json()
            else:
                response = "Error occurred when processing the request to url " + url
        elif operation == "Tf-Idf":

            # Process query and return response
            url = "http://127.0.0.1:8002/tf-idf/"

            response = requests.post(url, json={"corpus": documents, "query": prompt})
            if response.status_code == 200:
                response = response.json().get("response", "")
            else:
                response = "Error occurred when processing the request to url " + url
        else:
            response = "Please select either Late Chunking or Tf-Idf to perform an operation."
    except ValueError:
        # If the input is not a number, provide a static response
        response = "There was error , while processing your request !!."

    # Display assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)

    # Add assistant message to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
