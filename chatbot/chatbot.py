from chatbot.result_generator import generate_results
from chatbot.fake_review import create_fake_review
from utils.prompts import QUESTIONS

def run_chatbot():
    responses = {}
    print("영화 취향 테스트를 시작합니다!\n")

    for idx, question in enumerate(QUESTIONS, start=1):
        answer = input(f"{idx}. {question} (답변 입력): ")
        responses[f"Q{idx}"] = answer

    print("\n테스트 결과를 생성 중입니다...")
    results = generate_results(responses)
    print("\n[테스트 결과]")
    print(results)

    print("\n미리 쓰는 영화 리뷰 생성 중...")
    review = create_fake_review(results, responses)
    print("\n[미리 쓰는 영화리뷰]")
    print(review)
