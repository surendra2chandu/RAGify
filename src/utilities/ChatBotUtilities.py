# Import necessary libraries
import streamlit as st
import requests


class ChatBotUtilities:

    @staticmethod
    def show_chat_history(self):
        """
        This method displays the chat history.
        :return:
        """

        # Display chat history section
        if st.checkbox("Show Chat History"):
            st.write("### Chat History")

            # Display chat history if available
            if st.session_state.history:
                for user_input, bot_response in st.session_state.history:
                    st.write(f"**You**: {user_input}")
                    st.write(f"**Bot**:")
                    st.write(bot_response)
            else:
                # Display message if no chat history is available
                st.write("No chat history yet.")

    @staticmethod
    def handle_query(self, query, documents):
        """
        This method processes the query and returns the response.
        :param self: The object of the class
        :param query: The query entered by the user
        :param documents: The list of documents to compare the query with
        :return: The response to the query
        """

        # Process query and return response
        url = "http://127.0.0.1:8001/tf-idf/"

        response = requests.post(url, json={"corpus": documents, "query": query})
        if response.status_code == 200:
            res = response.json()
        else:
            res = {"response": "Error occurred when processing the request to url " + url}

        # Append query and response to chat history
        st.session_state.history.append((query, res))

        # Display response
        st.write("**Bot**:")
        st.write(res)
        # for line in res.split("\n"):
        #     st.write(line)

    @staticmethod
    def clear_chat_history(self):
        """
        This method clears the chat history.
        """

        # Button to clear chat history
        if st.button("Refresh"):
            st.session_state.history = []
