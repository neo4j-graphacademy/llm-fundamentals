import os
import openai
from neo4j import GraphDatabase, Result
import pandas as pd

openai.api_key = os.getenv("OPENAI_API_KEY")

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
)

driver.verify_connectivity()

movies = driver.execute_query("""
MATCH (m:Movie) WHERE m.plot IS NOT NULL
RETURN m.movieId AS movieId, m.title AS title, m.plot AS plot
LIMIT 1000
""",
result_transformer_=Result.to_df)

print(len(movies))

embeddings = []

for _, n in movies.iterrows():

    res = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=f"{n['title']}: {n['plot']}",
        encoding_format="float"
    )

    print(n['title'])

    embeddings.append({"movieId": n['movieId'], "embedding": res['data'][0]['embedding']})

embedding_df = pd.DataFrame(embeddings)
embedding_df.head()
embedding_df.to_csv('data\openai-embeddings.csv', index=False)
