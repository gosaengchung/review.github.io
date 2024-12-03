from flask import Flask, request, jsonify
from py2neo import Graph
from utils.neo4j_utils import load_data_to_neo4j, execute_neo4j_query
from utils.query_utils import parse_query
import pandas as pd
import os

# Flask 앱 생성
app = Flask(__name__)

# Neo4j 설정
NEO4J_URI = "neo4j+s://26c4eed1.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "7y4c467TrjPfdv44M5JbEHiR5YvWbzzuGn8mRk-gtik"

# Neo4j 연결
graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 데이터 로드
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")

# 데이터 적재
print("⏳ Neo4j에 데이터를 적재 중...")
load_data_to_neo4j(graph, movies, ratings)
print("✅ 데이터 적재 완료!")

# 기본 라우트
@app.route("/")
def home():
    return "🎬 영화 추천 챗봇 API가 실행 중입니다!"

# 영화 추천 API 엔드포인트
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    movie_title = data.get("movie_title", "")
    exclude_genres = data.get("exclude_genres", [])
    include_genres = data.get("include_genres", [])
    try:
        recommendations = execute_neo4j_query(graph, movie_title, exclude_genres, include_genres)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CLI 기반 영화 추천 챗봇
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

# 실행 조건
if __name__ == "__main__":
    # CLI 기반 챗봇 실행
    if os.environ.get("RUN_CLI") == "1":
        movie_chatbot()
    else:
        # Render에서 PORT 환경 변수 사용
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)

