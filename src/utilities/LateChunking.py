# Importing required libraries
from transformers import AutoTokenizer, AutoModel
import torch
from src.conf.Configurations import logger, model_path


class LateChunking:
    def __init__(self):
        """
        This function initializes the LateChunking class with the specified model path.
        """

        # Set the model name
        self.model_name = model_path

        # Load the tokenizer
        logger.info(f"Loading tokenizer from {self.model_name}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        # Load the model
        logger.info(f"Loading model from {self.model_name}...")
        self.model = AutoModel.from_pretrained(self.model_name)

    # Function to tokenize and generate embeddings
    def tokenize_and_embed(self, text, chunk_size=50):
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