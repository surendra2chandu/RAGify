import streamlit as st

# Define a simple chatbot class
class Chatbot:
    def __init__(self):
        # Initialize the chatbot responses dictionary
        self.responses = {
            "hello": "Hi there! How can I assist you today?",
            "how are you": "I am good, thanks for asking!",
            "bye": "Goodbye! Have a great day!",
        }

    # Method to fetch chatbot responses
    def get_responses(self, user_input):
        # Lookup the response for the user input; provide a default response if not found
        return self.responses.get(user_input.lower(), "Sorry, I didn't understand that. Can you ask something else?")

# Streamlit layout
def main():
    # Initialize session state variables
    if "chat_history" not in st.session_state:
        # Store chat history as a list of tuples (speaker, message)
        st.session_state.chat_history = []

    if "refresh_triggered" not in st.session_state:
        # Track whether the refresh button was pressed
        st.session_state.refresh_triggered = False

    # Initialize the Chatbot class
    chatbot = Chatbot()

    # Streamlit application title
    st.title("Simple Chatbot")
    st.write("Chat with me! Type something below:")

    # Create a text input for user input
    # 'key' ensures input persistence across reruns
    sample_user_input = st.text_input("Your Message:", key="user_input")

    # Refresh button to clear chat history
    if st.button("Refresh"):
        # Clear chat history and reset the refresh flag
        st.session_state.chat_history = []
        st.session_state.refresh_triggered = True

    # Process user input and update chat history
    if sample_user_input and not st.session_state.refresh_triggered:
        # Get chatbot response for user input
        response = chatbot.get_responses(sample_user_input)

        # Append the user's input and the bot's response to chat history
        st.session_state.chat_history.append(("You", sample_user_input))
        st.session_state.chat_history.append(("Bot", response))

        # Reset refresh flag after processing user input
        st.session_state.refresh_triggered = False

    # Display chat history
    st.write("### Chat History")
    if st.session_state.chat_history:
        # Display each message in chat history
        for speaker, message in st.session_state.chat_history:
            st.write(f"**{speaker}:** {message}")
    else:
        # Message displayed if chat history is empty
        st.write("No messages yet. Start chatting!")


# Main function
if __name__ == "__main__" :
    main()
