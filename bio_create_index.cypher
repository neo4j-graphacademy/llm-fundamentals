CALL db.index.vector.createNodeIndex(
    'personBiosEmbedding',
    'Person',
    'bioEmbedding',
    1536,
    'cosine'
)