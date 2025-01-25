# Importing the necessary libraries
import sys
import streamlit as st
sys.path.append(r'C:\PycharmProjects\RAGify')
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

        # button color
        bot.button_color(self)

        # Text input for query
        query = st.text_input("Enter your query:", key="query")

        if st.button("Late chunking"):
            if query:
                bot.retrive_chunks( query)
            else:
                st.write("Please enter a query.")

        # Add an Enter button
        if st.button("Submit"):
            if query:
                bot.handle_query(self, query, documents)
            else:
                st.write("Please enter a query.")


# Run the main function
if __name__ == "__main__":

    # Sample query
    sample_query = "sun"

    documents = [
        "The sun sets behind the mountains, casting a golden glow.",
        "The sun warmed the beach as we walked along the shore.",
        "She picked up her book and opened to the first page.",
        "After a long day, he relaxed with a hot cup of tea.",
        "The warmed air by the beach made the evening even more pleasant."
    ]

    # Initialize the ChatbotApp class
    app = ChatbotApp()

    # Run the main function
    app.main(sample_query)