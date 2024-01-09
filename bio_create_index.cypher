CALL db.index.vector.createNodeIndex(
    'personBio',
    'Person',
    'bioEmbedding',
    1536,
    'cosine'
)