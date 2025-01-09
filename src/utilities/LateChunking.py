# Importing required libraries
from src.conf.Configurations import logger
from src.utilities.EmbeddingUtility import EmbeddingUtility


class LateChunking:
    def __init__(self):
        """
        This function initializes the LateChunking class.
        """

        # Get the tokenizer
        self.tokenizer = EmbeddingUtility().get_tokenizer()

    # Late chunking function
    def late_chunk(self, tokens, embeddings, chunk_size=50):
        """
        This function chunks the tokens and embeddings.
        :param tokens: The tokens.
        :param embeddings: The embeddings.
        :param chunk_size: The chunk size.
        :return:
        """

        # Initialize the chunks list
        chunks = []

        # Loop through the tokens and embeddings
        logger.info("Chunking the tokens and embeddings...")
        for i in range(0, len(tokens), chunk_size):
            # Get the chunk tokens
            chunk_tokens = tokens[i:i + chunk_size]

            # Get the chunk embedding (mean of embeddings for the chunk)
            chunk_embedding = embeddings[i:i + chunk_size].mean(dim=0).numpy()

            # Get the chunk text
            chunk_text = self.tokenizer.convert_tokens_to_string(chunk_tokens).strip()

            # Append the chunk to the chunks list
            chunks.append((chunk_text, chunk_embedding))

        # Return the chunks
        return chunks