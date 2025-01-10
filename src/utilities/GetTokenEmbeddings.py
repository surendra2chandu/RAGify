# Importing required libraries
from src.conf.Configurations import logger
from src.utilities.EmbeddingUtility import EmbeddingUtility
import torch


class GetTokenEmbeddings:
    def __init__(self):
        """
        This function initializes the GetTokenEmbeddings class
        """

        # Get the tokenizer
        self.tokenizer = EmbeddingUtility().get_tokenizer()

        # Get the model
        self.model = EmbeddingUtility().get_model()

    # Function to tokenize and generate embeddings
    def tokenize_and_embed(self, text):
        """
        This function tokenizes the text and generates embeddings.
        :param text: The text to tokenize.
        :param chunk_size: The chunk size.
        :return: The tokens and embeddings.
        """

        # Tokenize the text
        logger.info("Tokenizing the text...")
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)

        # Generate embeddings
        with torch.no_grad():
            # Get the response from the model
            logger.info("Generating embeddings...")
            outputs = self.model(**inputs)

            # Get the embeddings from the response
            logger.info("Getting embeddings...")
            embeddings = outputs.last_hidden_state

        # Get the tokens
        logger.info("Converting input ids to tokens...")
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

        # Return the tokens and embeddings
        return tokens, embeddings[0]