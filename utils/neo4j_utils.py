from py2neo import Node, Relationship, Graph

def load_data_to_neo4j(graph, movies, ratings):
    # Neo4j 설정
    NEO4J_URI = "neo4j+s://26c4eed1.databases.neo4j.io"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "7y4c467TrjPfdv44M5JbEHiR5YvWbzzuGn8mRk-gtik"
    
    # Neo4j 연결
    graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    """Neo4j에 User, Movie 및 Rating 관계를 적재"""
    tx = graph.begin()
    
    # Movie 노드 생성
    for _, row in movies.iterrows():
        movie_node = Node("Movie", movieId=row["movieId"], title=row["title"], genres=row["genres"])
        tx.merge(movie_node, "Movie", "movieId")
    
    # User 노드 및 RATED 관계 생성
    for _, row in ratings.iterrows():
        user_node = Node("User", userId=row["userId"])
        movie_node = graph.nodes.match("Movie", movieId=row["movieId"]).first()
        if movie_node:
            rated_relationship = Relationship(user_node, "RATED", movie_node, rating=row["rating"], timestamp=row["timestamp"])
            tx.merge(user_node, "User", "userId")
            tx.merge(rated_relationship)
    # 트랜잭션 커밋
    tx.commit()
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
