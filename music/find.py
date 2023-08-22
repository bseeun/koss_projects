import pickle
import html

# 피클 파일 경로
file_path = 'music_data.pickle'

# 피클 파일 로드
with open(file_path, 'rb') as f:
    music_data = pickle.load(f, encoding='utf-8')

# 검색어 설정
search_query = 'make her dance'  # 'Inst'가 포함된 노래 검색

# 검색된 노래 개수 초기화
searched_songs = 0

# 검색된 노래와 인덱스 저장
search_results = []

# 검색된 노래 검색 및 결과 저장
for idx, data in enumerate(music_data):
    video_title = data['노래']
    video_url = data['URL']

    # 검색어가 노래 제목에 포함되는지 확인
    if search_query in video_title:
        searched_songs += 1
        # HTML 엔티티를 원래 문자로 변환
        video_title = html.unescape(video_title)

        search_results.append({'인덱스': idx, '노래': video_title, 'URL': video_url})

# 검색된 노래 개수 출력
print(f"검색된 노래 개수: {searched_songs}")

# 검색 결과 출력
for result in search_results:
    print(f"인덱스: {result['인덱스']}")
    print(f"노래: {result['노래']}")
    print(f"URL: {result['URL']}")
    print()

