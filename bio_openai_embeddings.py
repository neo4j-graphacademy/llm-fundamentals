import os
import csv

from openai import OpenAI
from neo4j import GraphDatabase

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def get_persons_bio(limit=None):
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD'))
    )

    driver.verify_connectivity()

    query = """MATCH (p:Person) WHERE p.bio IS NOT NULL
    RETURN p.tmdbId as tmdbId, p.name as name, p.bio as bio"""

    if limit is not None:
        query += f' LIMIT {limit}'

    persons, summary, keys = driver.execute_query(
        query
    )

    driver.close()

    return persons

def generate_embeddings(file_name, limit=None):

    csvfile_out = open(file_name, 'w', encoding='utf8', newline='')
    fieldnames = ['tmdbId','bio_embedding']
    output_bio = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    output_bio.writeheader()

    persons = get_persons_bio(limit=limit)

    print(len(persons))
    
    llm = OpenAI()

    for person in persons:
        print(person['tmdbId'], '-', person['name'])

        bio = person['bio'].replace('\n', ' ')
        response = llm.embeddings.create(
            input=bio,
            model='text-embedding-ada-002'
        )

        output_bio.writerow({
            'tmdbId': person['tmdbId'],
            'bio_embedding': response.data[0].embedding
        })

    csvfile_out.close()


# generate_embeddings('.\data\\person-bio-embeddings-1.csv',limit=1)
generate_embeddings('.\data\\person-bio-embeddings.csv')
