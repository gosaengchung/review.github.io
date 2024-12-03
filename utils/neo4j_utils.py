from py2neo import Node, Relationship

def load_data_to_neo4j(graph, movies, ratings):
    """Neo4j에 영화 데이터를 적재"""
    for _, row in merged_data.iterrows():
        movie_node = Node("Movie", movieId=row["movieId"], title=row["title"], genres=row["genres"])
        rating_node = Node("Rating", userId=row["userId"], rating=row["rating"], timestamp=row["timestamp"])
        relationship = Relationship(rating_node, "RATED", movie_node)
        graph.merge(movie_node, "Movie", "movieId")
        graph.merge(rating_node, "Rating", "userId")
        graph.merge(relationship)

def execute_neo4j_query(graph, movie_title, exclude_genres=None, include_genres=None):
    """Neo4j에서 조건에 따라 영화 추천"""
    cypher_query = f"""
    MATCH (m:Movie)-[:RATED]-(u:User)-[:RATED]->(rec:Movie)
    WHERE m.title = $movie_title
    """
    if exclude_genres:
        exclude_clause = " AND NOT any(genre IN split(rec.genres, '|') WHERE genre IN $exclude_genres)"
        cypher_query += exclude_clause
    if include_genres:
        include_clause = " AND any(genre IN split(rec.genres, '|') WHERE genre IN $include_genres)"
        cypher_query += include_clause

    cypher_query += """
    RETURN rec.title AS title, rec.genres AS genres, avg(rating) AS avg_rating
    ORDER BY avg_rating DESC LIMIT 5
    """

    result = graph.run(cypher_query, movie_title=movie_title, exclude_genres=exclude_genres, include_genres=include_genres)
    return [{"title": row["title"], "genres": row["genres"], "avg_rating": row["avg_rating"]} for row in result]
