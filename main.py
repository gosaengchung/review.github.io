from py2neo import Graph, Node, Relationship
from utils.neo4j_utils import load_data_to_neo4j, execute_neo4j_query
from utils.query_utils import parse_query
import pandas as pd

# Neo4j 설정
NEO4J_URI = "neo4j+s://26c4eed1.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "NpVvH9xz-99a30btrQfPxeCqt-kQc_XcmIlTeqNLpKg"

# Neo4j 연결
graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 데이터 로드
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# 데이터 적재
print("⏳ Neo4j에 데이터를 적재 중...")
load_data_to_neo4j(graph, movies, ratings)
print("✅ 데이터 적재 완료!")

# 영화 추천 챗봇
def movie_chatbot():
    print("🎬 영화 추천 챗봇에 오신 것을 환영합니다!")
    print("저는 영화와 관련된 질문에 대해 최적의 답변을 제공해드릴게요 😊\n")

    while True:
        query = input("🎥 질문을 입력하세요 (종료하려면 'exit' 입력): ")
        if query.lower() == "exit":
            print("🎬 감사합니다. 다음에 또 만나요!")
            break

        # 질문 처리 및 추천 영화 검색
        try:
            movie_title, exclude_genres, include_genres = parse_query(query)
            recommendations = execute_neo4j_query(graph, movie_title, exclude_genres, include_genres)

            if not recommendations:
                print(f"'{movie_title}'에 대한 조건을 만족하는 추천 영화를 찾을 수 없습니다.")
            else:
                print(f"'{movie_title}'와 관련된 추천 영화:")
                for rec in recommendations:
                    print(f"- {rec['title']} (Genres: {rec['genres']}, Avg. Rating: {rec['avg_rating']:.2f})")
        except Exception as e:
            print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    movie_chatbot()
