import os
import csv

from openai import OpenAI
from neo4j import GraphDatabase

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_movie_plots(limit=None):
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))
    )

    driver.verify_connectivity()

    query = """MATCH (m:Movie) WHERE m.plot IS NOT NULL
    RETURN m.movieId AS movieId, m.title AS title, m.plot AS plot"""

    if limit is not None:
        query += f' LIMIT {limit}'

    movies, summary, keys = driver.execute_query(
        query
    )

    driver.close()

    return movies

def generate_embeddings(file_name, limit=None):

    csvfile_out = open(file_name, 'w', encoding='utf8', newline='')
    fieldnames = ['movieId','embedding']
    output_plot = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    output_plot.writeheader()

    movies = get_movie_plots(limit=limit)

    print(len(movies))
    
    llm = OpenAI()

    for movie in movies:
        print(movie['title'])

        plot = f"{movie['title']}: {movie['plot']}"
        response = llm.embeddings.create(
            input=plot,
            model='text-embedding-ada-002'
        )

        output_plot.writerow({
            'movieId': movie['movieId'],
            'embedding': response.data[0].embedding
        })

    csvfile_out.close()

# generate_embeddings('.\data\\movie-plot-embeddings.csv',limit=1)
generate_embeddings('.\data\\movie-plot-embeddings.csv')
