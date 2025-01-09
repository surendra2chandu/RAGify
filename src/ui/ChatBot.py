#import
import streamlit as st

# Define a simple chatbot class
class Chatbot:

   def __init__(self):

    self.responses = {
        "hello": "Hi there! How can I assist you today?",
        "how are you ": "I am good, thanks for asking!",
        "bye": "Goodbye! Have a great day!",
    }

   def get_responses(self, user_input):
      return self.responses.get(user_input.lower(), "Sorry, I didn't understand that. Can you ask something else?")

if __name__ == "__main__":
    # Initialize the Chatbot class
    chatbot = Chatbot()

    # Streamlit layout
    st.title("Simple Chatbot")
    st.write("Chat with me! Type something below:")

    # Create a text input for user input
    sample_user_input = st.text_input("Your Message:")

    if sample_user_input:
      # Get chatbot response based on user input
      response = chatbot.get_responses(sample_user_input)

      # Display user input and bot response in the chat
      st.write(f"You: {sample_user_input}")
      st.write(f"Bot: {response}")
