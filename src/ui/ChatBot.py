# Importing the necessary libraries
import sys
import streamlit as st
sys.path.append('D:/RAGify')
from src.utilities.ChatBotUtilities import ChatBotUtilities

class ChatbotApp:
    def __init__(self):

        # Initialize chat history if not already set
        if 'history' not in st.session_state:
            st.session_state.history = []

    def main(self, query):
        # Initialize corpus

        bot = ChatBotUtilities()

        # Streamlit UI setup
        st.title("Simple Chatbot")

        # Clear chat history
        bot.clear_chat_history(self)

        # Show chat history
        bot.show_chat_history(self)

        # Text input for query
        query = st.text_input("Enter your query:")

        # Show results when query is entered
        if query:
            bot.handle_query(self, query, documents)

# Run the main function
if __name__ == "__main__":

    # Sample query
    sample_query = "adi narayana "

    documents = [
        "This is the first document",
        "This document is the second document",
        "And this is the third one",
        "Is this the first document adi",
        "Is this the first first document first adi narayana choudary reddy"
    ]

    # Initialize the ChatbotApp class
    app = ChatbotApp()

    # Run the main function
    app.main(sample_query)

