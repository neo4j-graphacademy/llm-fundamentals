LOAD CSV WITH HEADERS
FROM 'file:///person-bio-embeddings.csv'
AS row
MATCH (p:Person {tmdbId: row.tmdbId})
CALL db.create.setNodeVectorProperty(p, 'bioEmbedding', apoc.convert.fromJsonList(row.bio_embedding))