CALL db.index.vector.createNodeIndex(
    'moviePlotsEmbedding',
    'Movie',
    'plotEmbedding',
    1536,
    'cosine'
)