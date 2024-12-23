# server.py: REST API 서버 구현
from flask import Flask, request, jsonify
from py2neo import Graph
from utils.neo4j_utils import load_data_to_neo4j, execute_neo4j_query
from utils.query_utils import parse_query
import pandas as pd

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    """REST API로 영화 추천"""
    user_query = request.json.get('query', '')
    try:
        # 질문 처리 및 추천 검색
        movie_title, exclude_genres, include_genres = parse_query(user_query)
        recommendations = execute_neo4j_query(graph, movie_title, exclude_genres, include_genres)

        if not recommendations:
            return jsonify({"status": "error", "message": f"'{movie_title}'에 대한 추천 영화를 찾을 수 없습니다."})
        return jsonify({"status": "success", "data": recommendations})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
