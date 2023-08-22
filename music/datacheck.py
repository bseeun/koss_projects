import pickle

# 피클 파일 경로
pickle_file = "music_data.pickle"

# 피클 파일 열기
with open(pickle_file, 'rb') as file:
    # 피클 파일에서 객체 복원
    data = pickle.load(file)

# # 데이터의 100번째부터 200번째까지 출력
for item in data[2550:2600]:
    print(item)