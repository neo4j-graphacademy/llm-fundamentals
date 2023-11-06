import os
import openai
from neo4j import GraphDatabase, Result
import pandas as pd
from openai.error import APIError
from time import sleep

def generate_embeddings(file_name, limit=None):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    driver = GraphDatabase.driver(
        os.getenv("NEO4J_URI"),
        auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
    )

    driver.verify_connectivity()

    query = """MATCH (m:Movie) WHERE m.plot IS NOT NULL
    RETURN m.movieId AS movieId, m.title AS title, m.plot AS plot"""

    if limit is not None:
        query += f" LIMIT {limit}"

    movies = driver.execute_query(
        query,
        result_transformer_=Result.to_df
    )

    print(len(movies))
    
    embeddings = []

    for _, n in movies.iterrows():
        
        successful_call = False
        while not successful_call:
            try:
                res = openai.Embedding.create(
                    model="text-embedding-ada-002",
                    input=f"{n['title']}: {n['plot']}",
                    encoding_format="float"
                )
                successful_call = True
            except APIError as e:
                print(e)
                print("Retrying in 5 seconds...")
                sleep(5)

        print(n['title'])

        embeddings.append({"movieId": n['movieId'], "embedding": res['data'][0]['embedding']})

    embedding_df = pd.DataFrame(embeddings)
    embedding_df.head()
    embedding_df.to_csv(file_name, index=False)

generate_embeddings('data\openai-embeddings.csv',limit=1000)
generate_embeddings('data\openai-embeddings-full.csv',limit=None)