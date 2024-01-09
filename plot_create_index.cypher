CALL db.index.vector.createNodeIndex(
    'moviePlots',
    'Movie',
    'plotEmbedding',
    1536,
    'cosine'
)