import pickle
import os
from pytube import YouTube
import sttmusic
import torch

# 피클파일 해결하기

# 모델 로드하기
model = sttmusic.load_model("medium")

# 피클 파일 경로
music_data_pickle = "music_data.pickle"
music_res_pickle = "music_res.pickle"

# music_data.pickle 파일 로드
with open(music_data_pickle, 'rb') as file:
    music_data = pickle.load(file)

# 기존 결과 로드 또는 파일 생성
try:
    with open(music_res_pickle, 'rb') as file:
        music_res = pickle.load(file)
except FileNotFoundError:
    music_res = {}

# 가사 추출 함수
def whisperlyrics(audio_file_path):
    audio_file = open(audio_file_path, "rb")
    result = model.transcribe("song.mp3")
    lyrics = result["text"]
    return lyrics

# 음악 데이터 처리
for idx, song_data in enumerate(music_data[:5], 1):
    song_name = song_data['노래']
    song_url = song_data['URL']
    
    print(f"Processing Song {idx}: {song_name}")

    try:
        # MP4 파일 다운로드
        yt = YouTube(song_url)
        output_video = yt.streams.get_lowest_resolution().download(filename = 'video.mp4')
        
        output_audio = "audio.mp3"        

        # MP3 파일을 이용하여 가사 추출
        lyrics = whisperlyrics(output_video)
        print(lyrics)

        # 결과 저장
        song_data['가사'] = lyrics
        # music_res[song_name] = song_data  # Store song data in the music_res dictionary

        # MP3 파일 삭제
        os.remove(output_video)

    except Exception as e:
        print(f"Skipping Song {idx}: {song_name} ({str(e)})")
        continue

# music_res.pickle 파일에 결과 저장
with open(music_res_pickle, 'wb') as file:
    pickle.dump(music_res, file)
