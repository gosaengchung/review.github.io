from utils.data_loader import load_data, preprocess_data
from chatbot.recommender import calculate_similarity, recommend_movies

def run_chatbot():
    print("🎬 영화 추천 챗봇에 오신 것을 환영합니다!")
    
    # 데이터 로드 및 처리
    movies, ratings = load_data()
    movies, ratings, user_movie_matrix = preprocess_data(movies, ratings)
    
    # 유사도 매트릭스 계산
    similarity_matrix = calculate_similarity(user_movie_matrix)
    
    # 사용자 입력 받기
    user_input = input("어떤 영화를 좋아하나요? 영화 제목을 입력하세요: ")
    movie_id = movies[movies['title'] == user_input]['movieId'].values[0]

    print(f"'{user_input}'와 유사한 영화를 추천합니다...\n")
    recommendations = recommend_movies(movie_id, similarity_matrix, user_movie_matrix)
    
    for idx, (movie_id, rating) in enumerate(recommendations, start=1):
        movie_title = movies[movies['movieId'] == movie_id]['title'].values[0]
        print(f"{idx}. {movie_title} (예상 별점: {rating:.2f})")
