# Importing required libraries
from src.conf.Configurations import logger
from src.utilities.GetTokenEmbeddings import GetTokenEmbeddings
from src.utilities.DataBaseUtility import DataBaseUtility


class DataRetrival:

    def retrieve_relevant_text(self, query):
        """
        This function retrieves relevant text based on the query.
        :param query: The query to search for.
        :return: The relevant text.
        """

        # Tokenize and embed the query
        logger.info("Tokenizing and embedding the query...")
        res = GetTokenEmbeddings().tokenize_and_embed(query)

        # Get the mean of the embeddings
        logger.info("Getting the mean of the embeddings...")
        query_embedding = res[1].mean(dim=0).numpy()

        # Fetch similar text from the database
        logger.info("Fetching similar text from the database...")
        result = DataBaseUtility().fetch_similar_text(query_embedding)

        return result

if __name__ == "__main__":
    # Sample query
    sample_query = "who is narendra modi?"

    # Retrieve relevant text
    results = DataRetrival().retrieve_relevant_text(sample_query)

    for chunk, similarity in results:
        print(f"Chunk: {chunk}\nSimilarity: {similarity}\n")



