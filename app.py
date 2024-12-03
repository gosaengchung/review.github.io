from flask import Flask, request, jsonify, render_template
from py2neo import Graph
from utils.neo4j_utils import load_data_to_neo4j, execute_neo4j_query
from utils.query_utils import parse_query
import pandas as pd
import os

# Flask 애플리케이션 초기화
app = Flask(__name__)

# Neo4j 설정
NEO4J_URI = "neo4j+s://26c4eed1.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "NpVvH9xz-99a30btrQfPxeCqt-kQc_XcmIlTeqNLpKg"
try:
    graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    graph.run("RETURN 1")
    print("Neo4j 연결 성공!")
except Exception as e:
    print(f"Neo4j 연결 실패: {e}")
    
# Neo4j 데이터 로드 (한 번만 실행 필요)
movies = pd.read_csv("movies.csv")
ratings = pd.read_csv("ratings.csv")
load_data_to_neo4j(graph, movies, ratings)

# HTML 홈 페이지 라우트
@app.route("/")
def index():
    """메인 페이지"""
    return render_template("index.html")

# 추천 API 엔드포인트
@app.route("/recommend", methods=["POST"])
def recommend():
    """질문을 받아 추천 영화 반환"""
    user_query = request.json.get("query", "")
    if not user_query:
        return jsonify({"status": "error", "message": "질문이 비어 있습니다."})

    try:
        # 질문 처리 및 추천 검색
        movie_title, exclude_genres, include_genres = parse_query(user_query)
        recommendations = execute_neo4j_query(graph, movie_title, exclude_genres, include_genres)

        if not recommendations:
            return jsonify({"status": "error", "message": f"'{movie_title}'에 대한 추천 영화를 찾을 수 없습니다."})
        return jsonify({"status": "success", "data": recommendations})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# Flask 앱 실행
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
