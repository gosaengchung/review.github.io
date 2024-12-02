from flask import Flask, render_template, request, jsonify
from py2neo import Graph
from utils.neo4j_utils import load_data_to_neo4j, execute_neo4j_query
from utils.query_utils import parse_query
import pandas as pd

# Flask 애플리케이션 초기화
app = Flask(__name__)

# Neo4j 설정
NEO4J_URI = "neo4j+s://<cluster-id>.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "your-password"
graph = Graph(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# 데이터 로드 및 적재 (처음 실행 시 필요)
movies = pd.read_csv("data/movies.csv")
ratings = pd.read_csv("data/ratings.csv")
load_data_to_neo4j(graph, movies, ratings)

@app.route('/')
def index():
    """웹페이지 초기 화면"""
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    """추천 영화 처리"""
    try:
        # 사용자의 질문을 받아 파싱
        user_query = request.form['query']
        movie_title, exclude_genres, include_genres = parse_query(user_query)

        # Neo4j에서 추천 영화 검색
        recommendations = execute_neo4j_query(graph, movie_title, exclude_genres, include_genres)

        if not recommendations:
            return jsonify({"status": "error", "message": f"'{movie_title}'에 대한 조건을 만족하는 추천 영화를 찾을 수 없습니다."})
        
        # 결과 반환
        return jsonify({"status": "success", "data": recommendations})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
