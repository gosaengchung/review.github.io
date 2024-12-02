import pandas as pd

def load_data():
    # 영화 데이터 로드
    movies = pd.read_csv("data/movies.csv")
    ratings = pd.read_csv("data/ratings.csv")
    return movies, ratings

def preprocess_data(movies, ratings):
    # 사용자-아이템 평점 매트릭스 생성
    user_movie_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')
    return movies, ratings, user_movie_matrix
