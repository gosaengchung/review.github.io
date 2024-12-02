import re
from fuzzywuzzy import process

def parse_query(query: str):
    """질문에서 영화 제목과 조건 추출"""
    # 영화 제목 추출
    potential_titles = re.findall(r"[가-힣\w\s]+", query)
    potential_titles = ["".join(p.split()) for p in potential_titles]

    movie_title = None
    for candidate in potential_titles:
        match, score = process.extractOne(candidate, titles)
        if score >= 50:
            movie_title = match
            break

    # 조건 추출
    exclude_genres = re.findall(r"피하고\s싶어|제외", query)
    include_genres = re.findall(r"위주로\s추천|포함", query)

    exclude_genres_text = re.findall(r"[가-힣\w]+", query) if exclude_genres else []
    include_genres_text = re.findall(r"[가-힣\w]+", query) if include_genres else []

    return movie_title, exclude_genres_text, include_genres_text
