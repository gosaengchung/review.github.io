from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

def calculate_similarity(user_movie_matrix):
    # NaN을 0으로 대체하고 코사인 유사도 계산
    user_movie_matrix_filled = user_movie_matrix.fillna(0)
    similarity = cosine_similarity(user_movie_matrix_filled.T)
    return pd.DataFrame(similarity, index=user_movie_matrix.columns, columns=user_movie_matrix.columns)

def recommend_movies(movie_id, similarity_matrix, user_movie_matrix, top_n=5):
    # 입력한 영화와 유사한 영화 추천
    similar_movies = similarity_matrix[movie_id].sort_values(ascending=False).head(top_n + 1).iloc[1:]
    recommendations = []
    for movie in similar_movies.index:
        avg_rating = user_movie_matrix[movie].mean()
        recommendations.append((movie, avg_rating))
    return recommendations
